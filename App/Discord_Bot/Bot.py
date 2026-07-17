## IMPORTS ##
from typing import overload

import discord
from discord.message import Message
from App.Helpers.Response import Response

## CLASSES ##
class Bot(discord.Client):
  """The Discord Bot that interacts with the API.
  """

  ## VALUES ##
  API_KEY:str # The API Key associated with the Discord Bot.

  ## CONSTRUCTOR ##
  def __init__(self):
    pass
  # End of __init__()

  ## PUBLIC METHODS ##
  @overload
  async def on_ready(self) -> None:
    """Initialisation steps to make when the Bot connects to the Discord API.
    """
    pass
  # End of on_ready() 

  @overload
  async def on_message(self, message:discord.Message) -> None:
    """Receives a message from a discord server and delegates it to the appropriate client object.
    """
    pass
  # End of on_message() 

  @staticmethod
  def storeClient(clientID:str) -> Response:
    """Stores a client in the game's database.
    Args:
      clientID (str): The ID of the client to store in the game's database. Should be the same as the guild ID provided by discord.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of storeClient()

  @staticmethod
  def deleteClient(clientID:str) -> Response:
    """Deletes a client currently stored in the game's database.
    Removes all reference of the client, including any objects that use it as a partial key.
    If the client is currently cached, it will also remove the client from the cache.
    Args:
      clientID (str): The ID of the client to remove from the game's database. Should be the same as the guild ID provided by discord.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of deleteClient()
  
  @staticmethod
  def cacheClient(clientID:str) -> Response:
    """Moves a client from the game's database into the cache.
    If the client is already in the cache, it resets it's timer.
    Args:
      clientID (str): The ID of the client to cache. Should be the same as the guild ID provided by discord.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of cacheClient()

  @staticmethod
  def uncacheClient(clientID:str) -> Response:
    """Removes a client from the game's cache, but leaves it in the game's database.
    Args:
      clientID (str): The ID of the client to uncache. Should be the same as the guild ID provided by discord.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of uncacheClient()

  def getEvictionCandidates() -> list[str]:
    """Returns the oldest objects in the cache until there is enough space to add a new client.
    The oldest objects are not deleted by this function, and should be removed by the calling function as necessary.
    Removes any objects past their timeout, prior to finding the list of eviction candidates.
    Returns:
      list[str]: The list of the oldest objects in the cache. 
    """
    pass
  # End of getEvictionCandidates()

  ## PRIVATE METHODS ##
  def __loadAPIKey(self) -> None:
    """Loads the Bot's API key from the .env file. 
    """
    pass
  # End of loadAPIKey()

  async def __checkCache(self) -> None:
    """Periodically checks the cache for overflows and timed-out Clients.
    """
    pass
  # End of __checkCache()
# End of DQMBot