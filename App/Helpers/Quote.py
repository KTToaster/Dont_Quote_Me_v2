## IMPORTS ##
from dataclasses import dataclass


## CLASSES ##
@dataclass
class Quote():
  """A dataclass that holds all the data within of a quote
  """
  ## VALUES ##
  message_id:str  # The ID of the message that contained the quote.
  quote:str       # The actual quote that was said.
  quoted:str      # The alias of the person who was quoted.
  context:str     # The context attached to the quote.
  sent:int        # The UNIX timestamp of when the quote was sent.
# End of Quote