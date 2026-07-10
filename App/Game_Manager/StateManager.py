## IMPORTS ##
from App.Game_Manager.PlayerManager import PlayerManager
from App.Game_Manager.SettingsManager import SettingsManager
from App.Helpers.Quote import Quote
from App.Helpers.Response import Response

## CLASSES ##
class StateManager():
  """Handles the Game State of the current DQM session.
  """
  ## VALUES ##
  availableQuotes:list[Quote] # The quotes that can be used in the rounds.
  settings:SettingsManager    # The rules that the game has to follow.
  players:PlayerManager       # The players that can be quoted.

  ## CONSTRUCTOR ##
  def __init__(self):
    pass
  # End of __init__()
  
  ## PUBLIC METHODS ##
  def nextRound(self) -> Response:
    pass
  # End of nextRound()
  
  def endGame(self) -> Response:
    pass
  # End of endGame()

  ## PRIVATE METHODS ##
  def __fetchQuotes(self) -> Response:
    pass
  # End of __fetchQuotes()
# End of StateManager