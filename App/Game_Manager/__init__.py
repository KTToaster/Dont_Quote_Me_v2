from App.Helpers.Response import HELPDEFAULT, HELPPLAYERS, HELPSETTINGS, HELPSTATE, Response, ResponseCode


def __help(self, params:list[str]|None=None) -> Response:
  """Responds to a /help command
  Args:
    params (list[str] | None): A string broken into tokens indicating the parameters of the command. Defaults to None.
    Can include the command to get help for. Check Docs/command_grammar.md for full details.
  """
  paramCount = 0
  try:
    paramCount = len(params)
  except TypeError:
    return Response(ResponseCode.OK, HELPDEFAULT)
  if(paramCount == 0):
    return Response(ResponseCode.OK, HELPDEFAULT)
  elif(paramCount == 1):
    match(params[0].lower()):
      case "players":
        return Response(ResponseCode.OK, HELPPLAYERS)
      case "settings":
        return Response(ResponseCode.OK, HELPSETTINGS)
      case "state" | "play":
        return Response(ResponseCode.OK, HELPSTATE)
      case _:
        return Response(ResponseCode.BAD_REQUEST, f"""Invalid parameter {params[0]}.
        Use \"/help\" for a list of all commands.""")
  else:
    return Response(ResponseCode.BAD_REQUEST, f"""Invalid number of parameters. Expected 0 or 1, received: {paramCount}.""")
# End of help()