## IMPORTS ##
import discord

from App.Helpers.Response import Response

## CLASSES ##
class Bot(discord.Client):
  """The Discord Bot that interacts with the API.
  """

  ## VALUES ##
  API_KEY:str                   # The API Key associated with the Discord Bot.

  ## CONSTRUCTOR ##
  def __init__(self):
    pass
  # End of __init__()

  ## PUBLIC METHODS ##
  @staticmethod
  def storeClient(clientID:str) -> Response:
    pass
  # End of storeClient()

  @staticmethod
  def deleteClient(clientID:str) -> Response:
    pass
  # End of deleteClient()
  
  @staticmethod
  def cacheClient(clientID:str) -> Response:
    pass
  # End of cacheClient()

  @staticmethod
  def uncacheClient(clientID:str) -> Response:
    pass
  # End of uncacheClient()

  ## PRIVATE METHODS ##
  def __loadAPIKey(self) -> None:
    pass
  # End of loadAPIKey()
# End of DQMBot