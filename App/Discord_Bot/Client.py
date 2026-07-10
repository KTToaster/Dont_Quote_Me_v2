## IMPORTS ##
from discord.message import Message

from App.Discord_Bot import Scraper
from App.Game_Manager import SettingsManager
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
    pass
  # End of on_message()


  def sendMessage(self, channel:str, message:str) -> None:
    pass
  # End of sendMessage()
  
  ## PRIVATE METHODS ##
  def __help(self, params:list[str]) -> Response:
    pass
  # End of help()

  def __sync() -> None:
    pass
  # End of sync()
# End of Client