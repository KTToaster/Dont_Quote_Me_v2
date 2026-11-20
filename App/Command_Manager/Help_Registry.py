## IMPORTS ##
from collections.abc import Callable
from App.Helpers. Response import Response, ResponseCode

## STATIC METHODS ##
def _help(args:list[str]) -> Response:
  if len(args) == 0:
    return HELP_DEFAULT
  match args[0]:
    case "default":
      return HELP_DEFAULT
    case "players":
      return HELP_PLAYERS
    case "settings":
      return HELP_SETTINGS
    case _:
      return HELP_UNKNOWN
# End of _help()

## CONSTANTS ##
HELP_DEFAULT  = Response(ResponseCode.OK, """PLACEHOLDER: HELP_DEFAULT""")
HELP_PLAYERS  = Response(ResponseCode.OK, """PLACEHOLDER: HELP_PLAYERS""")
HELP_SETTINGS = Response(ResponseCode.OK, """PLACEHOLDER: HELP_SETTINGS""")
HELP_STATE    = Response(ResponseCode.OK, """PLACEHOLDER: HELP_STATE""")
HELP_UNKNOWN  = Response(ResponseCode.OK, """PLACEHOLDER: HELP_UNKNOWN""")


HELP_REGISTER: dict[str,Callable[[list[str]], Response]] = {
  "/help": _help 
}