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
  allPlayers:dict[str,list[str]]  # All the players that are associated with this client and their aliases.
  activePlayers:list[str]         # The players that can currently be quoted.
  
  ## CONSTRUCTOR ##
  def __init__(self, allPlayers:dict[str,list[str]]={}, activePlayers:list[str]={}):
    self.allPlayers=allPlayers
    self.activePlayers=activePlayers
  # End of __init__()
  
  ## PUBLIC METHODS ##
  def createPlayer(self, params:list[str]) -> Response:
    """Stores a player in the game's database.
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the player's name and aliases to add. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pLen = len(params)

    # Process parameters
    if(pLen == 0):
      return Response(ResponseCode.BAD_PARAMETERS, "Invalid Parameters: No player name given.")
    if(pLen > MAX_ALIASES):
      return Response(ResponseCode.BAD_PARAMETERS, f"Invalid Parameters: Too many aliases given. Max: {MAX_ALIASES}.")
    if(len(self.activePlayers) >= MAX_PLAYERS):
      return Response(ResponseCode.FORBIDDEN, f"Forbidden: Maximum number of players reached. Max: {MAX_PLAYERS}.")
    # Check player name is unique
    if(params[0] in self.allPlayers):
      return Response(ResponseCode.BAD_PARAMETERS, f"Invalid Parameters: Player already exists. Use /listplayers for a list of all players.")

    # Create player and aliases
    self.allPlayers[params[0]] = [params[0]]
    if(len(params) > 1):
      self.createAlias(params)

    return Response(ResponseCode.OK, f"Created Player \"{params[0]}\", with aliases {stringifyArray(params[1:])}") # TODO
  # End of createPlayer()
  
  def createAlias(self, params:list[str]) -> Response:
    """Adds an alias to an existing player, and stores it in the game's database. 
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the player's name and the aliases to add. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    # Process parameters
    pLen = len(params)
    if(pLen == 0):
      return Response(ResponseCode.BAD_PARAMETERS, "Invalid Parameters: No player name given.")
    if(params[0] not in self.allPlayers):
      return Response(ResponseCode.BAD_PARAMETERS, f"Invalid Parameters: Player \"{params[0]}\" not found. use /listplayers to see a list of all player names.")
    if(pLen < 2):
      return Response(ResponseCode.BAD_PARAMETERS, "Invalid Parameters: No aliases given.")
    if(pLen-1 + len(self.activePlayers[params[0]]) > MAX_ALIASES):
      return Response(ResponseCode.FORBIDDEN, f"Forbidden: Too many aliases given. Max: {MAX_ALIASES}.")

    # Add Aliases to player
    message = ""
    for i in range(1, len(params)):
      for name, aliases in self.allPlayers.items():
        if(params[i] in aliases): # Check Alias is unique
          message+=f"Invalid Parameter: Could not add alias \"{params[i]}\" to player \"{params[0]}\" as player \"{name}\" owns the alias.\n"
          continue
        message += f"Added Alias \"{params[i]}\" to player \"{params[0]}\"\n"
        self.allPlayers[params[0]].append(params[i])
    return Response(ResponseCode.OK, message)
  # End of createAlias()
  
  def addPlayer(self, params:list[str]) -> Response:
    """Adds a player to the list of people that can be quoted in the next game. Supports wildcards.
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the player's name and a flag to check aliases as the name. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    # Process parameters.
    params = [param for param in params if not param.startswith("-")]
    if(len(params) == 0):
      return Response(ResponseCode.BAD_PARAMETERS, "Invalid Parameters: No player name given.")
    if(len(params) + len(self.activePlayers) > MAX_ACTIVE_PLAYERS):
      return Response(ResponseCode.FORBIDDEN, f"Forbidden: Maximum number of active players reached. Max: {MAX_ACTIVE_PLAYERS}.")

    # Process flags
    flags = [flag.lower() for flag in params[1:] if flag.startswith("-")]
    strict = "-strict" in flags or "-s" in flags

    message = ""
    matched = False
    for pattern in params:
      for player in self.__matchPlayers(pattern.lower(), strict):
        if player in self.activePlayers:
          message += f"Found Player \"{player}\", but they are already active."
          continue
        matched = True
        message += f"Added \"{player}\" to the next session."

    return Response(ResponseCode.OK, message)
  # End of addPlayer()

  def deletePlayer(self, params:list[str]) -> Response:
    """Removes a player from the game's database, including all of their aliases. Supports wildcards. 
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the player's name and a flag to check aliases as the name. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    # Process parameters
    if(len(params) == 0):
      return Response(ResponseCode.BAD_PARAMETERS, "Invalid Parameters: No player name given.")
    # Process flags
    flags = [flag.lower() for flag in params[1:]]
    strict = "--strict" in flags or "-s" in flags

    # Remove players
    message=""
    for player in self.__matchPlayers(params[0], strict):
      self.allPlayers.pop(player)
      try: self.activePlayers.pop() # Remove player from activePlayers as well
      except KeyError: pass
      message += f"Deleted player \"{player}\".\n"

    if(message == ""):
      return Response(ResponseCode.NOT_FOUND, f"No player(s) found matching \"{params[0]}\".")
    return Response(ResponseCode.OK, message)
  # End of deletePlayer()

  def deleteAlias(self, params:list[str]) -> Response:
    """Removes an alias associated to a player from the game's database. Does not remove player names. Supports wildcards.
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the alias to remove. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    # Process parameters
    if(len(params) == 0):
      return Response(ResponseCode.BAD_PARAMETERS, "Invalid Parameters: No alias given.")
    pattern = params[0].lower()

    message = ""
    for name, aliases in self.allPlayers.items():
      if(fnmatch(name.lower(), pattern)): # Ignore player names.
        continue
      # Find alias
      for alias in aliases:
        if(fnmatch(alias.lower(), pattern)):
          self.allPlayers[name].pop(alias)
          try: self.activePlayers.pop() # Remove alias from activePlayers as well
          except KeyError: pass
          message += f"Removed alias \"{alias}\" from \"{name}\".\n"

    if(message == ""):
      return Response(ResponseCode.NOT_FOUND, f"No alias(es) found matching \"{params[0]}\".")
    return Response(ResponseCode.OK, message)
  # End of deleteAlias()

  def removePlayer(self, params:list[str]) -> Response:
    """Removes a player from the list of people that can be quoted in the next game. Supports wildcards.
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the player's name and a flag to check aliases as the name. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    # Process parameters
    if(len(params) == 0):
      return Response(ResponseCode.BAD_PARAMETERS, "Invalid Parameters: No player name given.")

    # Process flags 
    flags = [flag.lower() for flag in params[1:] if flag.startswith("-")]
    strict = "--strict" in flags or "-s" in flags

    message = ""
    for player in self.__matchPlayers(params[0], strict, True):
      self.activePlayers.pop()
      message += f"Removed {player}.\n"
    if(message == ""):
      return Response(ResponseCode.NOT_MODIFIED, "No player(s) to remove. Use /listactive to see a list of all active players.")
    return Response(ResponseCode.OK, message)
  
  # End of removePlayer()

  def listPlayers(self) -> Response:
    """Lists all the players associated with this client in the game's database.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    return Response(ResponseCode.OK, stringifyArray(self.allPlayers.keys(), "\n"))
  # End of listPlayers()

  def listActivePlayers(self) -> Response:
    """Lists all the players that can be quoted in the next game.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    return Response(ResponseCode.OK, stringifyArray(self.activePlayers.keys(), "\n"))
  # End of listActivePlayers()

  def playerDetails(self, params:list[str]) -> Response:
    """Shows the details of a player, including all their aliases. Supports wildcards.
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the player's name and a flag to check aliases as the name. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    flags = [flag.lower() for flag in params[1:] if flag.startswith("-")]
    strict = "--strict" in flags or "-s" in flags

    message = ""
    for player in self.__matchPlayers(params[0], strict):
      message += f"{player}: {"Active" if player in self.activePlayers else "Inactive"}\n"
      message += f"AKA: {stringifyArray(self.allPlayers[player])}\n\n"
    if(message == ""):
      return Response(ResponseCode.NOT_FOUND, "No player information to display. Check your spelling or pattern format.")
    return Response(ResponseCode.OK, message)
  # End of playerDetails()

  ## PRIVATE METHODS ##
  def __matchPlayers(self, pattern:str, strict:bool=False, activeOnly=False) -> list[str]:
    """Finds the players that match a given pattern (Case insensitive).
    Args:
      pattern (str): The pattern to match a name or alias to. Supports * and ? wildcards (see fnmatch).
      strict (bool): Whether or not to only match against names, not aliases. Defaults to False.
      activeOnly (bool): Whether or not to only search for active players, Defaults to False.
    Returns:
      list[str]: The names (dict keys) of all matching players.
    """
    pattern = pattern.lower() 
    searching = self.activePlayers if activeOnly else searching = self.allPlayers

    if(strict): # Search for names in keys
      return [name.lower() for name in searching if fnmatch(name.lower(), pattern)]

    # Search for names in alias
    players = []
    for name, aliases in searching.items():
      if(any(fnmatch(alias.lower(), pattern) for alias in aliases)):
        players.append(name)
    return players
  # End of __matchPlayers()
# End of PlayerManager