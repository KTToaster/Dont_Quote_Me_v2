## IMPORTS ##
from enum import Enum

from App.Helpers.Response import Response

## ENUMS ##
class GameTypes(Enum):
  FREE_FOR_ALL=1
  FIFTY_FIFTY=2

## CLASSES ##
class SettingsManager():
  """Manages the settings for the next DQM game.
  """
  ## VALUES ##
  roundLimit:int      # The maximum number of rounds to play.
  gameType:GameTypes  # The format of the game to play.
  useStrictNames:bool # Whether or not to allow aliases.
  quoteChannel:str    # The channel to scrape quotes from.
  scrapeFrom:int      # The first point of time that quotes can be found. Stored as a unix timestamp in seconds. 
  scrapeTo:int        # The last point of time that quotes can be found. Stored as a unix timestamp in seconds.
  
  ## CONSTRUCTOR ##
  def __init__(self):
    pass
  # End of __init__()

  
  ## PUBLIC METHODS ##
  def setRule(self, params:list[str]) -> Response:
    pass
  # End of setRule()

  def saveRuleset(self, params:list[str]) -> Response:
    pass
  # End of saveRuleset()

  def loadRuleset(self, params:list[str]) -> Response:
    pass
  # End of loadRuleset()

  def deleteRuleset(self, params:list[str]) -> Response:
    pass
  # End of deleteRuleset()
# End of SettingsManager