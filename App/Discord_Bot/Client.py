## IMPORTS ##
import shlex
from discord.message import Message
from discord.channel import TextChannel
from time import time

from App.Database import Database
from App.Discord_Bot.Scraper import Scraper
from App.Game_Manager.SettingsManager import SettingsManager
from App.Helpers.Response import *
from App.Game_Manager.PlayerManager import PlayerManager
from App.Game_Manager.StateManager import StateManager
from App.Command_Parser.Parser import Parser


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
  gameIndex:int             # Counts the number of games that have been played by this client.
  
  ## CONSTRUCTOR ##
  def __init__(self, id:int, loadVals:bool=True):
    """Creates a Client Object.
    Args:
      id (int): The ID of the guild that is being communicated with.
      loadVals (bool, optional): whether or not the client should load it's values from the database. Defaults to True.
    """
    self.ID = id
    if(loadVals):
      pass
    else:
      self.gameIndex = 0
    self.lastActivity = time()
  # End of __init__()
  
  
  ## PUBLIC METHODS ##
  async def on_message(self, message:Message) -> None:
    """Handles a message being sent to the discord server associated with this client.
    Args:
      message (Message): The message that has been sent to the client.
    """
    # Get commands and params
    tokenisedMessage = shlex.split(message.content)[1:]
    if len(tokenisedMessage) == 0:
      self.sendMessage(message.channel, self.__help())
      return
    
    # Match commands to their respective functions.
    res:Response
    try:
      match(tokenisedMessage[0].lower):
        case "/createplayer":     # Player Commands
          name = Parser.parseName(tokenisedMessage[1:])
          res = self.players.createPlayer(name)
        case "/createalias":
          name, aliases, flags = Parser.parseNameAliasesAndFlags(tokenisedMessage[1:])
          res = self.players.createAlias(name, aliases, flags)
        case "/addplayer":
          name, flags = Parser.parseNameAndFlags(tokenisedMessage[1:])
          res = self.players.addPlayer(name, flags)
        case "/deleteplayer":
          name, flags = Parser.parseNameAndFlags(tokenisedMessage[1:])
          res = self.players.deletePlayer(name, flags)
        case "/deletealias":
          name, flags = Parser.parseNameAndFlags(tokenisedMessage[1:])
          res = self.players.deleteAlias(name, flags)
        case "/removeplayer":
          name, flags = Parser.parseNameAndFlags(tokenisedMessage[1:])
          res = self.players.removePlayer(name, flags)
        case "/listplayers":
          res = self.players.listPlayers()
        case "/listactive":
          res = self.players.listActivePlayers()
        case "/inspectplayer":
          name, flags = Parser.parseNameAndFlags(tokenisedMessage[1:])
          res = self.players.inspectPlayer(name, flags)
        
        
        case "/quotechannel":     # Settings Commands
          channel = Parser.parseName(tokenisedMessage[1:])
          res = self.settings.setQuoteChannel(channel)
        case "/roundlimit":
          limit = Parser.parseNumber(tokenisedMessage[1:])
          res = self.settings.setRoundLimit(limit)
        case "/allowaliases":
          allow = Parser.parseBoolean(tokenisedMessage[1:])
          res = self.settings.allowAliases(allow)
        case "/scrapefrom":
          timestamp = Parser.parseDateTime(tokenisedMessage[1:])
          res = self.settings.setScrapeFrom(timestamp)
        case "/scrapeto":
          timestamp = Parser.parseDateTime(tokenisedMessage[1:])
          res = self.settings.setScrapeTo(timestamp)
        case "/scrapebetween":
          fromstamp, tostamp = Parser.parseDateTimes(tokenisedMessage[1:])
          res = self.settings.setScrapeBetween(fromstamp, tostamp)
        case "/saveruleset":
          name = Parser.parseName(tokenisedMessage[1:])
          res = self.settings.saveRuleset(name)
        case "/loadruleset":
          name = Parser.parseName(tokenisedMessage[1:])
          res = self.settings.loadRuleset(name)
        case "/deleteruleset":
          name, flags = Parser.parseNameAndFlags(tokenisedMessage[1:])
          res = self.settings.deleteRuleset(name, flags)
        case "/listrulesets":
          res = self.settings.listRulesets()
        case "/inspectruleset":
          name, flags = Parser.parseNameAndFlags(tokenisedMessage[1:])
          res = self.settings.inspectRuleset()


        case "/start":
          return
        case "/next":             # State Commands
          return
        case "/end":
          return
        case "/help":             # Help Commands
          self.sendMessage(message.channel, self.__help(tokenisedMessage[1:]))
          return
        case _:
          self.sendMessage(message.channel, Response(ResponseCode.BAD_REQUEST, f"""Unknown command \"{tokenisedMessage[0]}\".
                           Use \"/help\" for a list of all commands."""))
    except TypeError as e:
      res = Response(ResponseCode.BAD_REQUEST, e)  
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

  def __loadPlayers(self) -> Response:
    pass
  # End of __loadPlayers()

  def __loadSettings(self) -> Response:
    pass
  # End of __loadSettings()

  def __deloadPlayers(self) -> Response:
    if(self.players == None):
      return Response(ResponseCode.NOT_MODIFIED)
    # TODO: save and deload players
    pass
  # End of __deloadPlayers()

  def __deloadSettings(self) -> Response:
    if(self.settings == None):
      return Response(ResponseCode.NOT_MODIFIED)
    # TODO: save and deload settings
    pass
  # End of __deloadSettings()

  def __deloadState() -> None:
    pass
  # End of __deloadState()

  async def __sync(self) -> None:
    """Periodically updates the database with the changes made to the cached object.
    """
    pass
  # End of __sync()
# End of Client