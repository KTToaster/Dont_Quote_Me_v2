## IMPORTS ##
from App.Game_Manager.PlayerManager import PlayerManager
from App.Game_Manager.SettingsManager import SettingsManager
from App.Helpers.Quote import Quote
from App.Helpers.Response import Response

## CLASSES ##
class StateManager():
  """Handles the game state of the current DQM game.
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
    """Runs the next round of the current game.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of nextRound()
  
  def endGame(self) -> Response:
    """Ends the current game, resetting the available quotes.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of endGame()

  ## PRIVATE METHODS ##
  def __fetchQuotes(self) -> Response:
    """Fetches all the quotes that can be used in the game, upon start.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of __fetchQuotes()
# End of StateManager