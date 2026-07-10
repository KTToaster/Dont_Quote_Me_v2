## IMPORTS ##
from App.Discord_Bot.Client import Client
from App.Helpers.Response import Response
from App.Database import Database

## CLASSES ##
class Bot():
  """The Discord Bot that interacts with the API.
  """
  ## VALUES ##
  API_KEY:str                   # The API Key associated with the Discord Bot.

  CACHE_LENGTH:int              # The maximum number of clients stored in the clientCache Object.
  CACHE_TIMEOUT:int             # The maximum number of seconds to keep an unused client in the clientCache Object.
  clientCache:dict[str, Client] # The clients that are currently active.

  ## CONSTRUCTOR ##
  def __init__(self):
    """Creates a Bot Object
    """
    pass
  # End of __init__()
  
  
  ## PUBLIC METHODS ##
  def storeClient(clientID:str) -> Response:
    pass
  # End of storeClient()

  def deleteClient(clientID:str) -> Response:
    pass
  # End of deleteClient()
  
  def cacheClient(clientID:str) -> Response:
    pass
  # End of cacheClient()

  def uncacheClient(clientID:str) -> Response:
    pass
  # End of uncacheClient()

  ## PRIVATE METHODS ##
  def __loadAPIKey() -> None:
    pass
  # End of loadAPIKey()
# End of DQMBot