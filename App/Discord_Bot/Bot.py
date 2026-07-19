## IMPORTS ##
import asyncio
from time import time

import discord
from typing import overload

from Discord_Bot import *
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
  async def on_message(self, message:Message) -> None:
    """Receives a message from a discord server and delegates it to the appropriate client object.
    Args:
      message (Message): the message received from the discord server.
    """
    # Ignore own messages
    if(message.author.id == self.user.id):
      return
    
    # Ignore anything before command word (!DQM)
    commandIndex:int
    try:
      commandIndex = message.content.upper().index("!DQM") 
    except ValueError:
      return
    if not(commandIndex == 0 or message.content[commandIndex-1] != '\\'):
      return
    message.content = message.content[commandIndex:]

    # Delegate to client
    guildID = message.guild.id
    if(guildID in clientCache): # Check cache first to prevent wasted messages to the DB.
      clientCache[guildID].lastActivity = time()
    elif(guildID in self.listClients()):
      self.cacheClient(guildID)
    else:
      self.storeClient(guildID)
      self.cacheClient(guildID)
    clientCache[guildID].on_message(message)
  # End of on_message() 

  @staticmethod
  def storeClient(clientID:int) -> Response:
    """Stores a client in the game's database.
    Args:
      clientID (int): The ID of the client to store in the game's database. Should be the same as the guild ID provided by discord.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    # TODO Send SQL Command
    pass
  # End of storeClient()

  @staticmethod
  def deleteClient(clientID:int) -> Response:
    """Deletes a client currently stored in the game's database.
    Removes all reference of the client, including any objects that use it as a partial key.
    If the client is currently cached, it will also remove the client from the cache.
    Args:
      clientID (int): The ID of the client to remove from the game's database. Should be the same as the guild ID provided by discord.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    # TODO: Send SQL Command
    clientCache.pop(clientID)  
  # End of deleteClient()
  
  @staticmethod
  def cacheClient(clientID:int) -> Response:
    """Moves a client from the game's database into the cache.
    If the client is already in the cache, it resets it's timer.
    Args:
      clientID (str): The ID of the client to cache. Should be the same as the guild ID provided by discord.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    #TODO: Send SQL Command
    pass
  # End of cacheClient()

  @staticmethod
  def uncacheClient(clientID:int) -> Response:
    """Removes a client from the game's cache, but leaves it in the game's database.
    Args:
      clientID (str): The ID of the client to uncache. Should be the same as the guild ID provided by discord.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of uncacheClient()

  @staticmethod
  def getEvictionCandidates() -> list[int]:
    """Returns the oldest objects in the cache until there is enough space to add a new client.
    The oldest objects are not deleted by this function, and should be removed by the calling function as necessary.
    Removes any objects past their timeout, prior to finding the list of eviction candidates.
    Returns:
      list[str]: The list of the oldest objects in the cache. 
    """
    # Remove anything timed out.
    for id, client in clientCache.items():
      if(time() - client.lastActivity > CACHE_TIMEOUT):
        clientCache.pop(id)
    
    # Find eviction candidates
    toEvict = len(clientCache) - (CACHE_LENGTH - 1)
    evictionCandidates = []

    for id, client in clientCache.items():
      if(len(evictionCandidates) < toEvict):
        evictionCandidates.append(id)
      else:
        # TODO find N oldest candidates
        pass
    return evictionCandidates 
  # End of getEvictionCandidates()

  def listClients(self) -> list[int]:
    """Lists the IDs of all the clients in the database.
    """
    # TODO Send SQL command
    pass
  # End of listClients()

  ## PRIVATE METHODS ##
  def __loadAPIKey(self) -> None:
    """Loads the Bot's API key from the .env file. 
    """
    # TODO: Read .env file
    pass
  # End of loadAPIKey()

  async def __checkCache(self) -> None:
    """Periodically checks the cache for overflows and timed-out Clients.
    """
    while True:
      overflow = self.getEvictionCandidates()[1:]
      for client in overflow:
        clientCache.pop(client)
      asyncio.sleep(120)
  # End of __checkCache()
# End of DQMBot