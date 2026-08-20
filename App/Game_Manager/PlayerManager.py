## IMPORTS ##
from App.Helpers.Response import Response, ResponseCode

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
  def __init__(self):
    pass
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

    if(pLen == 0):
      return Response(ResponseCode.BAD_PARAMETERS, "Invalid Parameters: No player name given.")
    if(pLen > MAX_ALIASES):
      return Response(ResponseCode.BAD_PARAMETERS, f"Invalid Parameters: Too many aliases given. Max: {MAX_ALIASES}.")
    if(len(self.activePlayers.keys()) >= MAX_PLAYERS):
      return Response(ResponseCode.FORBIDDEN, f"Forbidden: Maximum number of players reached. Max: {MAX_PLAYERS}.")
    if(params[0] in self.allPlayers.keys()):
      return Response(ResponseCode.BAD_PARAMETERS, f"Invalid Parameters: Player already exists")

    self.allPlayers[params[0]] = [params[0]]
    if(len(params) > 1):
      self.createAlias(params)

    return Response(ResponseCode.OK, f"Created Player \"{params[0]}\", with aliases {"..."}") # TODO
  # End of createPlayer()
  
  def createAlias(self, params:list[str]) -> Response:
    """Adds an alias to an existing player, and stores it in the game's database. 
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the player's name and the aliases to add. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pLen = len(params)

    if(pLen == 0):
      return Response(ResponseCode.BAD_PARAMETERS, "Invalid Parameters: No player name given.")
    if(params[0] not in self.allPlayers.keys()):
      return Response(ResponseCode.BAD_PARAMETERS, "Invalid Parameters: Player not found. use /listPlayers to see a list of all player names.")
    if(pLen < 2):
      return Response(ResponseCode.BAD_PARAMETERS, "Invalid Parameters: No aliases given.")
    if(pLen-1 + len(self.activePlayers[params[0]]) > MAX_ALIASES):
      return Response(ResponseCode.FORBIDDEN, f"Forbidden: Too many aliases given. Max: {MAX_ALIASES}.")

    responseMessage = ""
    for i in range(1, len(params)):
      existsFlag = False
      for name, aliases in self.allPlayers.items():
        if(params[i] in aliases):
          responseMessage+=f"Invalid Parameter: Could not add alias \"{params[i]}\" to player \"{params[0]}\" as player \"{name}\" owns the alias."
      self.allPlayers[params[0]].append(params[i])
    

    return Response(ResponseCode.OK, f"Added Aliases {"..."} to player {params[0]}") # TODO

  # End of createAlias()
  
  def addPlayer(self, params:list[str]) -> Response:
    """Adds a player to the list of people that can be quoted in the next game. Supports wildcards.
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the player's name and a flag to check aliases as the name. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of addPlayer()

  def deletePlayer(self, params:list[str]) -> Response:
    """Removes a player from the game's database, including all of their aliases. Supports wildcards. 
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the player's name. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of deletePlayer()

  def deleteAlias(self, params:list[str]) -> Response:
    """Removes an alias associated to a player from the game's database. Supports wildcards.
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the alias to remove. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of deleteAlias()

  def removePlayer(self, params:list[str]) -> Response:
    """Removes a player from the list of people that can be quoted in the next game. Supports wildcards.
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the player's name and a flag to check aliases as the name. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of removePlayer()

  def listPlayers(self) -> Response:
    """Lists all the players associated with this client in the game's database.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of listPlayers()

  def listActivePlayers(self) -> Response:
    """Lists all the players that can be quoted in the next game.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of listActivePlayers()

  def playerDetails(self, params:list[str]) -> Response:
    """Shows the details of a player, including all their aliases. Supports wildcards.
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the player's name and a flag to check aliases as the name. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of playerDetails()
# End of PlayerManager