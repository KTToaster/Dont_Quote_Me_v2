## IMPORTS ##
from App.Helpers import stringifyArray
from App.Helpers.Response import Response, ResponseCode

from fnmatch import fnmatch

## CONSTANTS ##
MAX_PLAYERS = 64        # The maximum number of players each client is allowed.
MAX_ACTIVE_PLAYERS = 8  # The maximum number of players each client can have playing in a game.
MAX_ALIASES = 16        # The maximum number of aliases each player can have, including their original name.

## CLASSES ##
class PlayerManager():
  """Managers the players that can be quoted by the DQM bot.
  """
  ## VALUES ##
  allPlayers:dict[str,set[str]]  # All the players that are associated with this client and their aliases.
  activePlayers:set[str]         # The players that can currently be quoted.
  
  ## CONSTRUCTOR ##
  def __init__(self, allPlayers:dict[str,set[str]]={}, activePlayers:set[str]=set()):
    self.allPlayers=allPlayers
    self.activePlayers=activePlayers
  # End of __init__()
  
  ## PUBLIC METHODS ##
  def createPlayer(self, player:str) -> Response:
    """Adds a new player to the guild's list of players.
    Args:
      player (str): The name of the player to create.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    # Check player can be added
    if self.__matchPlayers(player, False, False, True):
      return Response(ResponseCode.BAD_REQUEST, f"Cannot add player as a player already has this name.")
    if len(self.allPlayers) > MAX_ACTIVE_PLAYERS:
      return Response(ResponseCode.FORBIDDEN, f"Maximum number of players reached. Max: {MAX_PLAYERS}.")

    self.allPlayers[player] = set()
    self.allPlayers[player].add(player)
    return Response(ResponseCode.OK, f"Created player \"{player}\".")
  # End of createPlayer()
  
  def createAlias(self, player:str, alias:str, *flags:str) -> Response:
    """Adds an alias to an existing player.
    Args:
      player (str): The name of the player to add an alias to.
      alias (str): The alias to add to the player.
      *flags (str):
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    # Check alias can be added
    if len(self.allPlayers[player]) >= MAX_ALIASES:
      return Response(ResponseCode.FORBIDDEN, f"Could not add \"{alias}\" to {player} as the alias limit has been reached.") 

    # Check alias is unique
    for name, existingAliases in self.allPlayers.items():
      if alias in existingAliases:
        if "force" in flags and alias != name:
          self.allPlayers[name].remove(alias)
        else: 
          return Response(ResponseCode.BAD_REQUEST, f"Could not add \"{alias}\" to {player}, as it already belongs to {name}.")

    # Add Alias
    self.allPlayers[player].add(alias)
    return Response(ResponseCode.OK, f"Added alias \"{alias}\" to {player}.")
  # End of createAlias()
  
  def addPlayer(self, pattern:str, *flags:str) -> Response:
    """Adds a player to the list of people that can be quoted in the next game. Supports wildcards.
    Args:
      pattern (str): The pattern used to identify players that can be quoted in the next game.
      *flags (str):
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    message = ""

    # Find players matching the pattern
    for player in self.__matchPlayers(pattern, "strict" in flags, "raw" in flags):
      self.activePlayers.add(player)
      message += f"Added \"{player}\" to the next session.\n"

    if(message == ""):
      return Response(ResponseCode.NOT_FOUND, f"No player(s) found matching \"{pattern}\".")
    return Response(ResponseCode.OK, message)
  # End of addPlayer()

  def deletePlayer(self, pattern:str, *flags:str) -> Response:
    """Removes a player from the game's database, including all of their aliases. Supports wildcards.
    Args:
      pattern (str): The pattern used to identify players that should be deleted.
      *flags (str):
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    message = ""
    # Find players matching the pattern
    for player in self.__matchPlayers(pattern, "strict" in flags, raw="raw" in flags):
      # Remove Players
      self.allPlayers.pop(player)
      if player in self.activePlayers:
        self.activePlayers.remove(player)
        message += f"Deleted player \"{player}\".\n"
        
    if(message == ""):
      return Response(ResponseCode.NOT_FOUND, f"No player(s) found matching \"{pattern}\".")
    return Response(ResponseCode.OK, message)
  # End of deletePlayer()

  def deleteAlias(self, pattern:str, *flags:str) -> Response:
    """Removes an alias associated to a player from the game's database. Does not remove player names. Supports wildcards.
    Args:
      pattern (str): The pattern used to identify the aliases to be deleted.
      *flags (str):
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    message = ""
    for name, aliases in self.allPlayers.items():
      if ((not "raw" in flags) and fnmatch(name.lower(), pattern)) or pattern == name:
        message += f"Found {name} but could not remove it as it is a name, not an alias."
        continue
      for alias in aliases:
        if ((not "raw" in flags) and fnmatch(alias.lower(), pattern)) or pattern == alias:
          self.allPlayers[name].remove(alias)
          message += f"Removed alias \"{alias}\" from \"{name}\".\n"

    if(message == ""):
      return Response(ResponseCode.NOT_FOUND, f"No player(s) found matching \"{pattern}\".")
    return Response(ResponseCode.OK, message)
  # End of deleteAlias()

  def removePlayer(self, pattern:str, *flags:str) -> Response:
    """Removes a player from the list of people that can be quoted in the next game. Supports wildcards.
    Args:
      pattern (str): The pattern used to identify players that should not be quoted in the next game.
      *flags (str):
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    message = ""
    for player in self.__matchPlayers(pattern, "strict" in flags, True, "raw" in flags):
      self.activePlayers.remove(player)
      message += f"Removed {player}.\n"
    if(message == ""):
      return Response(ResponseCode.NOT_FOUND, f"No player(s) found matching \"{pattern}\".")
    return Response(ResponseCode.OK, message)
  # End of removePlayer()

  def listPlayers(self) -> Response:
    """Lists all the players associated with this client in the game's database.
    """
    return Response(ResponseCode.OK, stringifyArray(self.allPlayers.keys(), "\n"))
  # End of listPlayers()

  def listActivePlayers(self) -> Response:
    """Lists all the players that will be quoted in the next game.
    """
    return Response(ResponseCode.OK, stringifyArray(self.activePlayers, "\n"))
  # End of listActivePlayers()

  def inspectPlayer(self, pattern:str, *flags:str) -> Response:
    """Shows the details of a player, including all their aliases. Supports wildcards.
    Args:
      pattern (str): The pattern used to identify players that can be quoted in the next game.
      *flags (str):
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    message = ""
    for player in self.__matchPlayers(pattern, "strict" in flags, raw="raw" in flags):
      message += f"{player}: {"Active" if player in self.activePlayers else "Inactive"}\n"
      message += f"AKA: {stringifyArray(self.allPlayers[player])}\n\n"

    if(message == ""):
      return Response(ResponseCode.NOT_FOUND, f"No player(s) found matching \"{pattern}\".")
    return Response(ResponseCode.OK, message)
  # End of inspectPlayer()

  def getActivePlayers(self) -> dict[str,set[str]]:
    res = {}
    for player in self.activePlayers():
      res[player] = self.allPlayers[player]
    return res
  # End of getActivePlayers()

  ## PRIVATE METHODS ##
  def __matchPlayers(self, pattern:str, strict:bool=False, activeOnly:bool=False, raw:bool=False) -> list[str]:
    """Finds the players that match a given pattern (Case insensitive).
    Args:
      pattern (str): The pattern to match a name or alias to. Supports * and ? wildcards (see fnmatch).
      strict (bool): Whether or not to only match against names, not aliases. Defaults to False.
      activeOnly (bool): Whether or not to only search for active players, Defaults to False.
      raw (bool): Whether or not to treat the pattern as a raw string. Defaults to False.
    Returns:
      list[str]: The names (dict keys) of all matching players.
    """
    pattern = pattern.lower() 
    searching = self.activePlayers if activeOnly else searching = self.allPlayers

    if strict: # Search for names in keys
      if raw:
        return [name.lower() for name in searching if name.lower == pattern]
      return [name.lower() for name in searching if fnmatch(name.lower(), pattern)]

    # Search for names in alias
    players = []
    for name, aliases in searching.items():
      if raw:
        if any(alias.lower() == pattern for alias in aliases):
          players.append(name)
      elif any(fnmatch(alias.lower(), pattern) for alias in aliases):
          players.append(name)
    return players
  # End of __matchPlayers()
# End of PlayerManager