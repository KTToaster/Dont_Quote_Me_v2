## IMPORTS ##
from App.Discord_Bot.Client import Client

## GLOBALS ##
CACHE_LENGTH:int              # The maximum number of clients stored in the clientCache Object.
CACHE_TIMEOUT:int             # The maximum number of seconds to keep an unused client in the clientCache Object.
clientCache:dict[str, Client] # The clients that are currently active.