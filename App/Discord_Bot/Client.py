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
    tokens = shlex.split(message.content)[1:]
    if len(tokens) == 0:
      self.sendMessage(message.channel, _help())
      return

    # TODO: Game_Manager Caching
    if (handler := HELP_REGISTER.get(tokens[0])) != None:
      res = handler(tokens[1:])
    elif (handler := PLAYER_REGISTER.get(tokens[0])) != None:
      res = handler(self.players, tokens[1:])
    elif (handler := SETTINGS_REGISTER.get(tokens[0])) != None:
      res = handler(self.settings, tokens[1:])
    elif (handler := STATE_REGISTER.get(tokens[0])) != None:
      res = handler(self.state, tokens[1:])
    else:
      res = Response(ResponseCode.BAD_REQUEST, f"Unknown command \"{tokens[0]}\". Use /help for a list of commands.")
      
    if type(res) == list[ResponseCode]:
      for r in res:
        self.sendMessage(message.channel, r)
    else:
      self.sendMessage(message.channel, r)
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