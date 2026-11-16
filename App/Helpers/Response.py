## IMPORTS ##
from dataclasses import dataclass
from enum import Enum

## CLASSES ##
class ResponseCode(Enum):
  """The Response Codes the DQM Client can return.
  Based off of the HTTP response status codes.
  """
  # SUCCESS #
  OK=200

  # REDIRECTION #
  NOT_MODIFIED=304    # A request has been made that has had no effect.
  REDIR_END=330       # A request to use next has been redirected to end the game.

  # CLIENT ERRORS #
  FORBIDDEN=403       # The client's request has bee rejected as they do not have permission.
  NOT_FOUND=404       # A file that the User has reqnuested could not be found.
  BAD_REQUEST=400     # Variation of BAD_REQUEST, a command the user sent was unknown. 

  # SERVER ERRORS #
  INTERNAL_ERROR=500  # An error occurred within the server.
# End of ResponseCodes

@dataclass
class Response():
  """A dataclass object that holds a success/error code of a response, and a message that can be returned to the user. 
  """
  ## VALUES ##
  responseCode:ResponseCode # The code that the operation responds with.
  message:str|None          # The message attached to the code.

  def responseString(self) -> str:
    """Formats the response to show both the code and the message.
    Returns:
      str: The formatted response.
    """
    return f"{self.responseCode}: {self.message}"
  # End of responseString()
# End of Response

## GLOBALS ##
# TODO: Fill Out Help Messages
HELPDEFAULT   = Response(ResponseCode.OK,
                         """PLACEHOLDER: HELPDEFAULT""")
HELPPLAYERS   = Response(ResponseCode.OK,
                         """PLACEHOLDER: HELPPLAYERS""")
HELPSETTINGS  = Response(ResponseCode.OK,
                         """PLACEHOLDER: HELPSETTINGS""")
HELPSTATE     = Response(ResponseCode.OK,
                         """PLACEHOLDER: HELPSTATE""")