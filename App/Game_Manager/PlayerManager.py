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
    pass
  # End of createPlayer()
  
  def createAlias(self, params:list[str]) -> Response:
    pass
  # End of createAlias()
  
  def addPlayer(self, params:list[str]) -> Response:
    pass
  # End of addPlayer()

  def deletePlayer(self, params:list[str]) -> Response:
    pass
  # End of deletePlayer()

  def deleteAlias(self, params:list[str]) -> Response:
    pass
  # End of deleteAlias()

  def removePlayer(self, params:list[str]) -> Response:
    pass
  # End of removePlayer()

  def clearPlayers(self) -> Response:
    pass
  # End of clearPlayers()

  def clearAliases(self, params:list[str]) -> Response:
    pass
  # End of clearAliases()

  def listPlayers(self) -> Response:
    pass
  # End of listPlayers()

  def listActivePlayers(self) -> Response:
    pass
  # End of listActivePlayers()

  def playerDetails(self, params:list[str]) -> Response:
    pass
  # End of playerDetails()
# End of PlayerManager