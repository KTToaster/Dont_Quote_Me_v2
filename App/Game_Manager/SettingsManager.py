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
    """Updates a rule in the currently active ruleset. Does not change the rule in the game's database.
    saveRuleset must be called for permanent changes.
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the rule to change, and it's new value. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of setRule()

  def saveRuleset(self, params:list[str]|None=None) -> Response:
    """Saves the current ruleset to the game's database.
    Args:
      params (list[str] | None): A string broken into tokens indicating the parameters of the command. Defaults to None.
      Can include the name of the ruleset. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of saveRuleset()

  def loadRuleset(self, params:list[str]) -> Response:
    """Sets the current ruleset to match one in the game's database.
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the name of the ruleset. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of loadRuleset()

  def deleteRuleset(self, params:list[str]) -> Response:
    """Removes a ruleset from the game's database. Supports wildcards.
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the name of the ruleset. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of deleteRuleset()
# End of SettingsManager