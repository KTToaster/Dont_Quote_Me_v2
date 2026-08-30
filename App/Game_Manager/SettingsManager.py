## IMPORTS ##
from enum import Enum

from App.Helpers.Response import Response

## CONSTANTS ##
MAX_RULESETS=10  # The maximum number of rulesets each server is allowed

## ENUMS ##
class GameType(Enum):
  FREE_FOR_ALL=1
  FIFTY_FIFTY=2

## CLASSES ##
class SettingsManager():
  """Manages the settings for the next DQM game.
  """
  ## VALUES ##
  quotesChannel:int # The channel to scrape quotes from.
  roundLimit:int    # The maximum number of rounds to play. When negative, there is no limit on the number of rounds to play. 
  gameType:GameType # The format of the game to play.
  allowAliases:bool # Whether or not to allow aliases while scraping.
  scrapeFrom:int    # The first point of time that quotes can be found. Stored as a unix timestamp in seconds. When negative, there is no limit to when the quotes can be scraped from.
  scrapeTo:int      # The last point of time that quotes can be found. Stored as a unix timestamp in seconds. When negative, there is no limit to when the quotes can be scraped to.
  
  ## CONSTRUCTOR ##
  def __init__(self, quotesChannel:int, roundLimit:int=-1, gameType:GameType=GameType.FREE_FOR_ALL,
               allowAliases:bool=False, scrapeFrom:int=-1, scrapeTo:int=-1):
    self.quotesChannel = quotesChannel
    self.roundLimit = roundLimit
    self.gameType = gameType
    self.allowAliases = allowAliases
    self.scrapeFrom = scrapeFrom
    self.scrapeTo = scrapeTo
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
    match(params[0].lower):
      case "quoteschannel":
        return self.__quotesChannel(params[1:])
      case "roundlimit":
        return self.__roundLimit(params[1:])
      case "gametype":
        return self.__gameType(params[1:])
      case "allowaliases":
        return self.__allowAliases(True)
      case "disallowaliases":
        return self.__allowAliases(False)
      case "scrapefrom":
        return self.__scrapeFrom(params[1:])
      case "scrapeto":
        return self.__scrapeTo(params[1:])
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

  ## PRIVATE METHODS ##
  def __quotesChannel(self, params:list[str]) -> Response:
    pass
  # End of __quotesChannel()

  def __roundLimit(self, params:list[str]) -> Response:
    pass
  # End of __roundLimit()

  def __gameType(self, params:list[str]) -> Response:
    pass
  # End of __gameType()

  def __allowAliases(self, allow:bool) -> Response:
    pass
  # End of __allowAliases()


  def __scrapeFrom(self, params:list[str]) -> Response:
    pass
  # End of __scrapeFrom()

  def __scrapeTo(self, params:list[str]) -> Response:
    pass
  # End of __scrapeTo()

  def __scrapeBetween(self, params:list[str]) -> None:
    pass
  # End of __scrapeBetween()
# End of SettingsManager