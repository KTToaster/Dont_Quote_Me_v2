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
  responseCode:ResponseCode
  message:str
# End of Response