## IMPORTS ##
from collections.abc import Callable
from App.Helpers. Response import Response, Status

## STATIC METHODS ##
def _help(args:list[str]) -> Response:
  """Generates and returns appropriate help messages to the user.
  Args:
    args (list[str]): The user's message in tokenised form, indicating the type of help message to return.
  Returns:
    Response: A response consisting of a operation status code and a message that can be returned to the user.
  """
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
      return Response(Status.BAD_REQUEST, f"Unknown Help command {args[0]}. Use /help for a list of all commands.") 
# End of _help()

## CONSTANTS ##
HELP_DEFAULT  = Response(Status.OK, """PLACEHOLDER: HELP_DEFAULT""")
HELP_PLAYERS  = Response(Status.OK, """PLACEHOLDER: HELP_PLAYERS""")
HELP_SETTINGS = Response(Status.OK, """PLACEHOLDER: HELP_SETTINGS""")
HELP_STATE    = Response(Status.OK, """PLACEHOLDER: HELP_STATE""")


HELP_REGISTER: dict[str,Callable[[list[str]], Response]] = {
  "/help": _help 
}