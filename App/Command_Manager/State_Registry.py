## IMPORTS ##
from collections.abc import Callable

from App.Game_Manager.StateManager import StateManager
from App.Helpers.Response import Response

## STATIC METHODS ##
def _play(state:StateManager) -> Response:
  """Registers the `StateManager.play()` command.
  Args:
    settings (SettingsManager): The StateManager that invokes the command.
  Returns:
    Response: A response consisting of a operation status code and a message that can be returned to the user.
  """
  return state.play()
# End of _play()

def _end(state:StateManager) -> Response:
  """Registers the `StateManager.endGame()` command.
  Args:
    settings (SettingsManager): The StateManager that invokes the command.
  Returns:
    Response: A response consisting of a operation status code and a message that can be returned to the user.
  """
  return state.endGame()
# End of _end()

## CONSTANTS ##
STATE_REGISTER: dict[str,Callable[[StateManager], Response]] = {
  "/play": _play,
  "/next": _play,
  "/end": _end
}