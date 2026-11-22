## IMPORTS ##
import asyncio
from os import getenv
import discord
from time import time
from typing import overload
from discord.message import Message
from dotenv import load_dotenv

from Discord_Bot import *
from App.Helpers.Response import Response
from App.Helpers import stringifyArray

## CLASSES ##
class Bot(discord.Client):
  """The Discord Bot that interacts with the API.
  """
  ## VALUES ##
  API_KEY:str # The API Key associated with the Discord Bot.

  ## CONSTRUCTOR ##
  def __init__(self):
    self.__loadAPIKey()
  # End of __init__()

  ## PUBLIC METHODS ##
  @overload
  async def on_ready(self) -> None:
    """Initialisation steps to make when the Bot connects to the Discord API.
    """
    print("Don't Quote Me Bot Online.\nKnown Clients: ")
    print(stringifyArray(self.listClients()))
    self.__checkCache()
  # End of on_ready() 

  @overload
  async def on_message(self, message:Message) -> None:
    """Receives a message from a discord server and delegates it to the appropriate client object.
    Args:
      message (Message): the message received from the discord server.
    """
    # Ignore own messages
    if message.author.id == self.user.id:
      return
    
    print("Received Message:", " "*4, message) 
    # Ignore anything before command word (!DQM)
    commandIndex:int
    try:
      commandIndex = message.content.upper().index("!DQM") 
    except ValueError:
      return
    if commandIndex != 0 and message.content[commandIndex-1] == '\\': # Ignore Escaped Command Words
      return
    message.content = message.content[commandIndex:]

    # Delegate to client
    guildID = message.guild.id
    if guildID in clientCache: # Check cache first to prevent wasted messages to the DB.
      clientCache[guildID].lastActivity = time()
    elif guildID in self.listClients():
      self.cacheClient(guildID)
    else:
      self.storeClient(guildID)
      clientCache[guildID] = Client(guildID, False)
    clientCache[guildID].on_message(message)
  # End of on_message() 

  @staticmethod
  def storeClient(clientID:int) -> None:
    """Stores a client in the game's database.
    Args:
      clientID (int): The ID of the client to store in the game's database. Should be the same as the guild ID provided by discord.
    """
    # TODO Insert client into database
  # End of storeClient()

  @staticmethod
  def deleteClient(clientID:int) -> None:
    """Deletes a client currently stored in the game's database.
    Removes all reference of the client, including any objects that use it as a partial key.
    If the client is currently cached, it will also remove the client from the cache.
    Args:
      clientID (int): The ID of the client to remove from the game's database. Should be the same as the guild ID provided by discord.
    """
    # TODO: Delete client from database
    clientCache.pop(clientID) # Remove from cache as well
  # End of deleteClient()
  
  @staticmethod
  def cacheClient(clientID:int) -> None:
    """Moves a client from the game's database into the cache.
    If the client is already in the cache, it resets it's timer.
    Args:
      clientID (int): The ID of the client to cache. Should be the same as the guild ID provided by discord.
    """
    if clientID not in clientCache:
      clientCache[clientID] = Client(clientID)
    clientCache[clientID].lastActivity = time()
  # End of cacheClient()

  @staticmethod
  def uncacheClient(clientID:int) -> None:
    """Removes a client from the game's cache, but leaves it in the game's database.
    Args:
      clientID (int): The ID of the client to uncache. Should be the same as the guild ID provided by discord.
    """
    clientCache[clientID].deloadState()
    clientCache[clientID].deloadSettings()
    clientCache[clientID].deloadPlayers()
    # TODO: Update last activity in DB
    clientCache.pop(clientID)
  # End of uncacheClient()

  @staticmethod
  def getEvictionCandidates() -> list[Client]:
    """Returns the oldest objects in the cache until there is enough space to add a new client.
    The oldest objects are not deleted by this function, and should be removed by the calling function as necessary.
    Removes any objects past their timeout, prior to finding the list of eviction candidates.
    Returns:
      list[Client]: The list of the oldest objects in the cache. 
    """
    # Remove anything timed out.
    timedOut:list[int] = []
    for id, client in clientCache.items():
      if time() - client.lastActivity > CACHE_TIMEOUT:
        timedOut.append(id) # Store timed out and delete after the dict has been iterated through - prevents RunTimeErrors.
    for id in timedOut:
      clientCache.pop(id)

    # Find eviction candidates.
    toEvict = len(clientCache) - (CACHE_LENGTH - 1)
    if toEvict <= 0: # Check if eviction is needed.
      return []
    evictionCandidates = sorted(clientCache.values(), key=lambda client: client.lastActivity)
      
    return evictionCandidates[:toEvict]
  # End of getEvictionCandidates()

  def listClients(self) -> list[int]:
    """Lists the IDs of all the clients in the database.
    Returns:
      list[int]: All the IDs of the clients in the database
    """
  # End of listClients()

  ## PRIVATE METHODS ##
  def __loadAPIKey(self) -> None:
    """Loads the Bot's API key from the .env file. 
    """
    if load_dotenv():
      self.API_KEY = getenv("DISCORD_API_KEY")
      if self.API_KEY == None:
        raise NameError("DISCORD_API_KEY not found in .env file.")
      return
    raise FileNotFoundError("Could not find .env file.")
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