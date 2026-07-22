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

  # CLIENT ERRORS #
  BAD_COMMAND=460     # Variation of BAD_REQUEST, a command the user sent was unknown. 
  BAD_PARAMETERS=461  # Variation of BAD_REQUEST, the parameters of a known command were invalid.
# End of ResponseCodes

@dataclass
class Response():
  """A dataclass object that holds a success/error code of a response, and a message that can be returned to the user. 
  """
  ## VALUES ##
  responseCode:ResponseCode # The code that the operation responds with.
  message:str               # The message attached to the code.
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