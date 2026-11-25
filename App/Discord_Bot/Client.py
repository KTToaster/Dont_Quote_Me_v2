## IMPORTS ##
import shlex
import asyncio
from discord.message import Message
from discord.channel import TextChannel
from time import time

from App.Command_Manager.Help_Registry import HELP_REGISTER, _help
from App.Command_Manager.Player_Registry import PLAYER_REGISTER
from App.Command_Manager.Settings_Registry import SETTINGS_REGISTER
from App.Command_Manager.State_Registry import STATE_REGISTER
from App.Database import Database
from App.Discord_Bot import SYNC_TIMER
from App.Discord_Bot.Scraper import Scraper
from App.Game_Manager.SettingsManager import GameType, Ruleset, SettingsManager
from App.Helpers.Response import *
from App.Game_Manager.PlayerManager import PlayerManager
from App.Game_Manager.StateManager import StateManager


## CLASSES ##
class Client():
  """Handles communication for a specific guild/Discord server.
  """
  ## VALUES ##
  ID:int                    # The ID of the guild that is being communicated with.
  players:PlayerManager     # The object that handles the players for this guild.
  settings:SettingsManager  # The object that handles the settings for this guild.
  state:StateManager        # The object that handles the game state for this guild.
  scraper:Scraper           # The object that can scrape this guild.
  lastActivity:float        # The last time the guild was communicated with. 
  __playersSynced:bool      # Whether or not the PlayerManager has already been synchronised during the loop.
  __settingsSynced:bool     # Whether or not the SettingsManager has already been synchronised during the loop.

  
  ## CONSTRUCTOR ##
  def __init__(self, id:int):
    """Creates a Client Object.
    Args:
      id (int): The ID of the guild that is being communicated with.
      loadVals (bool, optional): whether or not the client should load it's values from the database. Defaults to True.
    """
    self.ID = id
    self.lastActivity = time()
    self.__sync()
  # End of __init__()
  
  
  ## PUBLIC METHODS ##
  async def on_message(self, message:Message) -> None:
    """Handles a message being sent to the discord server associated with this client.
    Args:
      message (Message): The message that has been sent to the client.
    """
    # Get commands and params
    tokens = shlex.split(message.content)[1:]
    if len(tokens) == 0:
      self.sendMessage(message.channel, _help())
      return
    self.lastActivity = time()
    tokens[0] = tokens[0].lower()

    if (handler := HELP_REGISTER.get(tokens[0])) != None:
      res = handler(tokens[1:])
    elif (handler := PLAYER_REGISTER.get(tokens[0])) != None:
      if(self.state == None):
        res = handler(self.__getPlayers(), tokens[1:])
      else:
        res = Status(Status.FORBIDDEN, "Player details cannot be modified during a game. Use /end to end the current session and modify players.")
    elif (handler := SETTINGS_REGISTER.get(tokens[0])) != None:
      if(self.state == None):
        res = handler(self.__getSettings(), tokens[1:])
      else:
        res = Status(Status.FORBIDDEN, "Settings cannot be modified during a game. Use /end to end the current session and modify settings.")
    elif (handler := STATE_REGISTER.get(tokens[0])) != None:
      res = handler(self.__getState())
      if  tokens[0] == "/end" and res.status == 200:
        self.__deloadState()
    else:
      res = Response(Status.BAD_REQUEST, f"Unknown command \"{tokens[0]}\". Use /help for a list of commands.")
      
    if type(res) == list[Status]:
      for r in res:
        self.sendMessage(message.channel, r)
    else:
      self.sendMessage(message.channel, res)
  # End of on_message()

  async def sendMessage(self, channel:TextChannel, message:Response) -> None:
    """Sends a message to the discord guid associated with this client. 
    Args:
      channel (TextChannel): The channel to send the message to.
      message (Response): The message to send to the channel.
    """
    channel.send(message.message)
  # End of sendMessage()

  def deloadPlayers(self) -> None:
    """Saves the cached PlayerManager to the Database and removes it from memory.
    """
    if self.players == None:
      return
    playerVals = []
    aliasVals = []
    for name, aliases in self.players.allPlayers.items():
      playerVals.append((self.ID, name, name in self.players.activePlayers))
      for alias in aliases:
        aliasVals.append((self.ID, alias, name))
    Database.execute("DELETE FROM players WHERE guild_id = %s", (self.ID), commit=False)
    if playerVals != []:
      Database.executeMany("""INSERT INTO players 
      (guild_id, player_name, is_active) 
      VALUES (%s, %s, %s);""", playerVals, False)
    if aliasVals != []:
      Database.executeMany("""INSERT INTO aliases 
      (guild_id, alias_name, player_name) 
      VALUES (%s, %s, %s);""", aliasVals)
    self.players = None
  # End of __deloadPlayers()

  def deloadSettings(self) -> None:
    """Saves the cached SettingsManager to the Database and removes it from memory.
    """
    if self.settings == None:
      return
    self.__syncSettings()
    self.settings = None
  # End of __deloadSettings()

  def deloadState(self) -> None:
    self.state = None
  # End of __deloadState()

  ## PRIVATE METHODS ##
  def __getPlayers(self) -> PlayerManager:
    """Returns the current PlayerManager for this Client. 
    If the PlayerManager is not cached, it will load it from the database and cache it.
    If there is no PlayerManager in the database, it will create a new one and cache it.
    Returns:
      PlayerManager: The current PlayerManager for this client.
    """
    if self.players != None:
      return self.players
    self.__syncPlayers()
    return self.players
  # End of __getPlayers()

  def __getSettings(self) -> SettingsManager:
    """Returns the current SettingsManager for this Client. 
    If the SettingsManager is not cached, it will load it from the database and cache it.
    If there is no SettingsManager in the database, it will create a new one and cache it.
    Returns:
      SettingsManager: The current SettingsManager for this client.
    """
    if self.settings != None:
      return self.settings
    rulesets:dict[str,Ruleset] = {}
    activeRuleset = "Default"
    for name, isActive, roundLimit, gameType, allowAliases, quotesChannel, scrapeFrom, scrapeTo in Database.fetchAll(
    "SELECT * FROM rulesets WHERE guild_id = %s", (self.ID,)):
      rulesets[name] = Ruleset(quotesChannel, name, roundLimit, GameType(gameType), allowAliases, scrapeFrom, scrapeTo)
      if isActive:
        activeRuleset = name
    self.settings = SettingsManager(rulesets, activeRuleset)
    return self.settings
  # End of __getSettings()

  def __getState(self) -> StateManager:
    """Returns the current StateManager for this Client.
    Un-caches the current PlayerManager and SettingsManager, as they cannot be accessed during gameplay.
    Returns:
      StateManager: The current StateManager for this Client.
    """
    if self.state != None:
      return self.state
    self.state = StateManager(self.ID,  self.__getSettings().getActiveRuleset(), self.__getPlayers().getActivePlayers())
    self.__deloadPlayers()
    self.__deloadSettings()
    return self.state
  # End of __getState()

  def __syncPlayers(self) -> None:
    """Updates the database with the changes made to the cache PlayerManager object. 
    """
    allPlayers:dict[str,set[str]] = {}
    activePlayers = set()
    for name, is_active, alias in Database.fetchAll(
    """SELECT p.player_name, p.is_active, a.alias_name 
    FROM players AS p LEFT JOIN aliases AS a 
    ON a.guild_id = p.guild_id AND a.player_name = p.player_name 
    WHERE p.guild_id = %s""", (self.ID)):
      if name not in allPlayers:
        allPlayers[name] = {name}
      allPlayers[name].add(alias)
      if is_active:
        activePlayers.add(name)
    self.players = PlayerManager(allPlayers, activePlayers)
    self.__playersSynced = True
  # End of __syncPlayers()

  def __syncSettings(self) -> None:
    """Updates the database with the changes made to the cache SettingsManager object. 
    """
    rulesetVals = []
    for name, ruleset in self.settings.rulesets.items():
      rulesetVals.append((self.ID, name, name==self.settings.activeRuleset, ruleset.roundLimit, ruleset.gameType.value, ruleset.allowAliases, ruleset.quotesChannel, ruleset.scrapeFrom, ruleset.scrapeTo))
    Database.execute("DELETE FROM rulesets WHERE guild_id = %s;", (self.ID), commit=False)
    Database.executeMany("""INSERT INTO rulesets 
    (guild_id, ruleset_name, is_active, round_limit, game_type, strict_names, channel_id, scrape_from, scrape_to) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""", rulesetVals)
    self.__settingsSynced = True
  # End of __syncSettings()

  async def __sync(self) -> None:
    """Periodically updates the database with the changes made to the cached objects.
    """
    while True:
      asyncio.sleep(SYNC_TIMER)
      if not self.__playersSynced:
        self.__syncPlayers()
      if not self.__settingsSynced:
        self.__syncSettings()
      self.__playersSynced = False
      self.__settingsSynced = False
  # End of __sync()
# End of Client