## IMPORTS ##
import shlex
from discord.message import Message
from discord.channel import TextChannel
from time import time

from App.Command_Manager.Help_Registry import HELP_REGISTER, _help
from App.Command_Manager.Player_Registry import PLAYER_REGISTER
from App.Command_Manager.Settings_Registry import SETTINGS_REGISTER
from App.Command_Manager.State_Registry import STATE_REGISTER
from App.Discord_Bot.Scraper import Scraper
from App.Game_Manager.SettingsManager import SettingsManager
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
  
  ## CONSTRUCTOR ##
  def __init__(self, id:int):
    """Creates a Client Object.
    Args:
      id (int): The ID of the guild that is being communicated with.
      loadVals (bool, optional): whether or not the client should load it's values from the database. Defaults to True.
    """
    self.ID = id
    self.lastActivity = time()
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
    tokens[0] = tokens[0].lower()

    if (handler := HELP_REGISTER.get(tokens[0])) != None:
      res = handler(tokens[1:])
    elif (handler := PLAYER_REGISTER.get(tokens[0])) != None:
      if(self.state == None):
        res = handler(self.__getPlayers(), tokens[1:])
      else:
        res = ResponseCode(ResponseCode.FORBIDDEN, "Player details cannot be modified during a game. Use /end to end the current session and modify players.")
    elif (handler := SETTINGS_REGISTER.get(tokens[0])) != None:
      if(self.state == None):
        res = handler(self.__getSettings(), tokens[1:])
      else:
        res = ResponseCode(ResponseCode.FORBIDDEN, "Settings cannot be modified during a game. Use /end to end the current session and modify settings.")
    elif (handler := STATE_REGISTER.get(tokens[0])) != None:
      res = handler(self.__getState())
      if  tokens[0] == "/end" and res.responseCode == 200:
        self.state = None
    else:
      res = Response(ResponseCode.BAD_REQUEST, f"Unknown command \"{tokens[0]}\". Use /help for a list of commands.")
      
    if type(res) == list[ResponseCode]:
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

  def __getPlayers(self) -> PlayerManager:
    if self.players != None:
      return self.players
    # TODO: load from DB
  # End of __getPlayers()

  def __getSettings(self) -> SettingsManager:
    if self.settings != None:
      return self.settings
    # TODO: load from DB
  # End of __getSettings()

  def __getState(self) -> StateManager:
    if self.state != None:
      return self.state
    self.state = StateManager(self.ID,  self.__getSettings().getActiveRuleset(), self.__getPlayers().getActivePlayers())
    self.__deloadPlayers()
    self.__deloadSettings()
    return self.state

  # End of __getState()

  def __deloadPlayers(self) -> Response:
    if self.players == None:
      return Response(ResponseCode.NOT_MODIFIED)
    # TODO: save and deload players
    pass
  # End of __deloadPlayers()

  def __deloadSettings(self) -> Response:
    if self.settings == None:
      return Response(ResponseCode.NOT_MODIFIED)
    # TODO: save and deload settings
    pass
  # End of __deloadSettings()

  def __deloadState(self) -> None:
    if self.state == None:
      return Response(ResponseCode.NOT_MODIFIED)
    self.state = None
    return Response(ResponseCode.OK)
  # End of __deloadState()

  async def __sync(self) -> None:
    """Periodically updates the database with the changes made to the cached object.
    """
    pass
  # End of __sync()
# End of Client