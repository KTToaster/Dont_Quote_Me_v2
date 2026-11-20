## IMPORTS ##
from collections.abc import Callable

from App.Command_Manager.Parser import Parser
from App.Game_Manager.StateManager import StateManager
from App.Helpers.Response import Response

## STATIC METHODS ##
def _play(state:StateManager) -> Response:
  return state.play()
# End of _play()

def _end(state:StateManager) -> Response:
  return state.endGame()
# End of _end()

## CONSTANTS ##
STATE_REGISTER: dict[str,Callable[[StateManager], Response]] = {
  "/play": _play,
  "/next": _play,
  "/end": _end
}