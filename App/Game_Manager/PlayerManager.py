## IMPORTS ##
from App.Helpers.Response import Response

## CLASSES ##
class PlayerManager():
  """Managers the players that can be quoted by the DQM bot.
  """
  ## VALUES ##
  playerAliases:dict[str,str] # The players that can currently be quoted and their aliases.
  
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
    pass
  # End of createPlayer()
  
  def createAlias(self, params:list[str]) -> Response:
    """Adds an alias to an existing player, and stores it in the game's database. 
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the player's name and the aliases to add. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
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