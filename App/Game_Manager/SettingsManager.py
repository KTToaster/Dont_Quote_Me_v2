## IMPORTS ##
from dataclasses import dataclass
from enum import Enum

from App.Helpers.Response import Response, ResponseCode

## CONSTANTS ##
MAX_RULESETS=10  # The maximum number of rulesets each server is allowed


## ENUMS ##
class GameType(Enum):
  FREE_FOR_ALL=1
  FIFTY_FIFTY=2

GAMETYPES_STR = {
  "ffa":GameType.FREE_FOR_ALL,
  "free-for-all":GameType.FREE_FOR_ALL,
  "fifty-fifty":GameType.FIFTY_FIFTY,
  "50/50":GameType.FIFTY_FIFTY
}

@dataclass
class Ruleset():
  quotesChannel:str                       # The ID of the channel to scrape quotes from.
  name:str="Default"                      # The Name that identifies the ruleset
  roundLimit:int=-1                       # The maximum number of rounds to play. When negative, there is no limit on the number of rounds to play. 
  gameType:GameType=GameType.FREE_FOR_ALL # The format of the game to play.
  allowAliases:bool=True                  # Whether or not to allow aliases while scraping.
  scrapeFrom:int=-1                       # The first point of time that quotes can be found. Stored as a unix timestamp in seconds. When negative, there is no limit to when the quotes can be scraped from.
  scrapeTo:int=-1                         # The last point of time that quotes can be found. Stored as a unix timestamp in seconds. When negative, there is no limit to when the quotes can be scraped to.

## CLASSES ##
class SettingsManager():
  """Manages the settings for the next DQM game.
  """
  ## VALUES ##
  rulesets:dict[str,Ruleset]
  activeRuleset:Ruleset

  ## CONSTRUCTOR ##
  def __init__(self, rulesets:dict[str,Ruleset]|None=None, quotesChannel:str|None=None, activeRuleset:str="Default"):
    if(rulesets == None and quotesChannel == None):
      raise AttributeError("Rulesets and channel cannot both be None.")
    elif(rulesets == None):
      self.rulesets = {"Default": Ruleset(quotesChannel=quotesChannel, name="Default")}
      self.activeRuleset = self.rulesets["Default"]

    self.rulesets = rulesets
    if(activeRuleset in rulesets): 
      self.activeRuleset = self.rulesets[activeRuleset]
    else:
      self.activeRuleset = self.rulesets["Default"]

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
        return self.__allowAliases(params[1:])
      case "scrapefrom":
        return self.__scrapeFrom(params[1:])
      case "scrapeto":
        return self.__scrapeTo(params[1:])
      case _:
        return Response(ResponseCode.BAD_COMMAND, f"Unknown Command: \"{params[0]}\". Use \"/help settings\" for a list of all settings commands.")
  # End of setRule()

  def saveRuleset(self, params:list[str]|None=None) -> Response:
    """Saves the current ruleset to the game's database.
    Args:
      params (list[str] | None): A string broken into tokens indicating the parameters of the command. Defaults to None.
      Can include the name of the ruleset. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    if(len(params) == 0):
      self.rulesets[self.activeRuleset.name] = self.activeRuleset
      return Response(ResponseCode.OK, f"Updated \"{self.activeRuleset.name}\" to current rules.")
    if(not params[0] in self.rulesets and self.rulesets+1 > MAX_RULESETS):
      return Response(ResponseCode.FORBIDDEN, f"Could not create new ruleset \"{params[0]}\" from current rules as the maximum number of rulesets ({MAX_RULESETS}) has been reached.")
    self.rulesets[params[0]] = self.activeRuleset
    return Response(ResponseCode.OK, f"Updated \"{self.activeRuleset.name}\" to current rules.")
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

  def listRulesets(self) -> Response:
    pass
  # End of listRulesets()

  def rulesetDetails(self, params:list[str]) -> Response:
    message = f"{self.rulesets[self.activeRuleset]}\n"

    return Response(Response.OK, message)
  # End of rulesetDetails()

  ## PRIVATE METHODS ##
  def __quotesChannel(self, params:list[str]) -> Response:
    """Sets the channel that the bot scrapes quote from.
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the id of the channel to scrape from. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    if(len(params) == 0):
      return Response(ResponseCode.BAD_PARAMETERS, "Invalid Parameters: No Channel ID given.")
    # TODO: Check if channel exists
    self.rulesets[self.activeRuleset] = params[0]
    return Response(ResponseCode.OK, f"Set Quotes Channel to \"{params[0]}\".")
  # End of __quotesChannel()

  def __roundLimit(self, params:list[str]) -> Response:
    """Sets the channel that the bot scrapes quote from.
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the number of rounds to play. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    if(len(params) == 0):
      return Response(ResponseCode.BAD_PARAMETERS, "Invalid Parameters: No round number given.")
    elif(params[0].lower() == "none"):
      self.rulesets[self.activeRuleset].roundLimit = -1
      return Response(ResponseCode.OK, "Removed round Limit")
    elif(params[0].isdigit()):
      self.rulesets[self.activeRuleset].roundLimit = int(params[0])
      return Response(ResponseCode.OK, f"Set round limit to {params[0]}")
    return Response(ResponseCode.BAD_PARAMETERS, "Invalid Parameters: Invalid round number.")
  # End of __roundLimit()

  def __gameType(self, params:list[str]) -> Response:
    """Sets the channel that the bot scrapes quote from.
    Args:
      params (list[str]): A string broken into tokens indicating the parameters of the command.
      Should include the number type of game to play. Check Docs/command_grammar.md for full details.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    if(len(params) == 0):
      return Response(ResponseCode.BAD_PARAMETERS, "Invalid Parameters: No round number given.")
    elif(params[0].lower() in GAMETYPES_STR):
      return # TODO
    
    return Response(ResponseCode.BAD_PARAMETERS, "Invalid Parameters: Invalid round number.")
    
  # End of __gameType()

  def __allowAliases(self, params:list[str]) -> Response:
    
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