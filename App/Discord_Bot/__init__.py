## IMPORTS ##
from App.Discord_Bot.Client import Client

## GLOBALS ##
CACHE_LENGTH:int = 32               # The maximum number of clients stored in the clientCache Object.
CACHE_TIMEOUT:int = 600             # The maximum number of seconds to keep an unused client in the clientCache Object.
SYNC_TIMER:int = 30                 # The number of seconds to wait between synchronisation of a cached Object.
clientCache:dict[int, Client] = {}  # The clients that are currently active.