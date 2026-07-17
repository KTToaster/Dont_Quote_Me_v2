## IMPORTS ##
from dataclasses import dataclass
from enum import Enum

## CLASSES ##
class ResponseCode(Enum):
  OK=200
# End of ResponseCodes

@dataclass
class Response():
  """A dataclass object that holds a success/error code of a response, and a message that can be returned to the user. 
  """
  ## VALUES ##
  responseCode:ResponseCode # The code that the operation responds with.
  message:str               # The message attached to the code.
# End of Response