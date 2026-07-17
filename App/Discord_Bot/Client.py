## IMPORTS ##
from discord.message import Message
from discord.channel import TextChannel

from App.Discord_Bot.Scraper import Scraper
from App.Game_Manager.SettingsManager import SettingsManager
from App.Helpers.Response import Response
from App.Game_Manager.PlayerManager import PlayerManager
from App.Game_Manager.StateManager import StateManager

## CLASSES ##
class Client():
  """Handles communication for a specific guild/Discord server.
  """
  ## VALUES ##
  ID:str                    # The ID of the guild that is being communicated with
  players:PlayerManager     # The object that handles the players for this guild.
  settings:SettingsManager  # The object that handles the settings for this guild.
  state:StateManager        # The object that handles the game state for this guild.
  scraper:Scraper           # The object that can scrape this guild.
  lastActivity:int          # The last time the guild was communicated with. 
  
  ## CONSTRUCTOR ##
  def __init__(self):
    pass
  # End of __init__()
  
  
  ## PUBLIC METHODS ##
  def on_message(self, message:Message) -> None:
    """Handles a message being sent to the discord server associated with this client.
    Args:
      message (Message): The message that has been sent to the client.
    """
    pass
  # End of on_message()

  def sendMessage(self, channel:TextChannel, message:str) -> None:
    """Sends a message to the discord guid associated with this client. 
    Args:
      channel (TextChannel): The channel to send the message to.
      message (str): The message to send to the channel.
    """
    pass
  # End of sendMessage()
  
  ## PRIVATE METHODS ##
  def __help(self, params:list[str]|None=None) -> Response:
    """Responds to a /help command
    Args:
      params (list[str] | None): A string broken into tokens indicating the parameters of the command. Defaults to None.
      Can include the command to get help for. Check Docs/command_grammar.md for full details.
    """
    pass
  # End of help()
# End of Client