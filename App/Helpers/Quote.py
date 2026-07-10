## IMPORTS ##
from dataclasses import dataclass


## CLASSES ##
@dataclass
class Quote():
  """A dataclass that holds all the data within of a quote
  """
  ## VALUES ##
  sender:str
  quote:str
  quoted:str
  context:str
# End of Quote