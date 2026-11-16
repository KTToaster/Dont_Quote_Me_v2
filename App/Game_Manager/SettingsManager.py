## IMPORTS ##
from dataclasses import dataclass
from enum import Enum
from datetime import datetime as dt
from fnmatch import fnmatch

from App.Helpers.Response import Response, ResponseCode

## CONSTANTS ##
MAX_RULESETS=8  # The maximum number of rulesets each server is allowed

## ENUMS ##
class GameType(Enum):
  FREE_FOR_ALL=1

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
  activeRuleset:str

  ## CONSTRUCTOR ##
  def __init__(self, rulesets:dict[str,Ruleset]|None=None, quotesChannel:str|None=None, activeRuleset:str="Default"):
    if rulesets == None and quotesChannel == None:
      raise AttributeError("Rulesets and channel cannot both be None.")
    elif rulesets == None:
      self.rulesets = {"Default": Ruleset(quotesChannel=quotesChannel, name="Default")}
      self.activeRuleset = "Default"

    self.rulesets = rulesets
    if activeRuleset in rulesets: 
      self.activeRuleset = self.rulesets[activeRuleset]
    else:
      self.activeRuleset = self.rulesets["Default"]

  # End of __init__()

  ## PUBLIC METHODS ##
  def saveRuleset(self, name:str|None) -> Response:
    """Saves the current ruleset to the game's database.
    Args:
      name (str | None): The name to save the ruleset as. Overwrites the current ruleset if none.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    if name == None or name == "":
      self.rulesets[self.activeRuleset.name] = self.activeRuleset
      return Response(ResponseCode.OK, f"Updated \"{self.activeRuleset.name}\" to current rules.")
    if not name in self.rulesets and self.rulesets+1 > MAX_RULESETS:
      return Response(ResponseCode.FORBIDDEN, f"Could not create new ruleset \"{name}\" from current rules as the maximum number of rulesets ({MAX_RULESETS}) has been reached.")
    self.rulesets[name] = self.activeRuleset
    return Response(ResponseCode.OK, f"Updated \"{self.activeRuleset.name}\" to current rules.")
  # End of saveRuleset()

  def loadRuleset(self, name:str) -> Response:
    """Sets the current ruleset to match one in the game's database.
    Args:
      name (str): The name of the ruleset to set as the current ruleset.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    if not name in self.rulesets:
      return Response(ResponseCode.BAD_REQUEST, f"Could not load ruleset \"{name}\" as it does not exist.")
    self.activeRuleset = name
    return Response(ResponseCode.OK, f"Using ruleset \"{name}\".")
    pass
  # End of loadRuleset()

  def deleteRuleset(self, pattern:str, *flags:str) -> Response:
    """Removes a ruleset from the game's database. Supports wildcards.
    Args:
      pattern (str): The pattern of rulesets to delete.
      *flags (str):
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    message = ""
    for ruleset in self.rulesets:
      if ((not "raw" in flags) and fnmatch(ruleset, pattern)) or pattern == ruleset:
        if ruleset == "Default":
          message += "Cannot delete Default ruleset.\n"
          continue
      self.rulesets.pop(ruleset)
      message += f"Deleted ruleset \"{ruleset}\".\n"
    return Response(ResponseCode.OK, message)
  # End of deleteRuleset()

  def listRulesets(self) -> Response:
    """Returns the names of all the rulesets associated with this guild.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    message = ""
    for ruleset in self.rulesets:
      message += ruleset + "\n"
    return Response(ResponseCode.OK, message)
  # End of listRulesets()

  def inspectRuleset(self, pattern:str|None, *flags) -> Response:
    """Returns the details of a ruleset from the game's database. Supports wildcards.
    Args:
      pattern (str): The pattern of rulesets to retrieve details on. Returns details on the active ruleset if None.
      *flags (str):
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    # TODO
    message = f"{self.rulesets[self.activeRuleset]}\n"
    return Response(Response.OK, message)
  # End of inspectRuleset()

  def setQuoteChannel(self, channel:str) -> Response:
    """Sets the channel that the bot scrapes quote from.
    Args:
      channel (str): The ID of the channel to scrape quotes from.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    # TODO: Check if channel exists

    self.rulesets[self.activeRuleset].quotesChannel = channel
    return Response(ResponseCode.OK, f"Set Quotes Channel to \"{channel}\".")
  # End of setQuoteChannel()

  def setRoundLimit(self, limit:int|None) -> Response:
    """Limits the number of rounds the next session can have.
    Args:
      limit (int | None): The number of rounds the next session can have.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    if limit == None or limit < 0:
      self.rulesets[self.activeRuleset].roundLimit = -1
      return Response(ResponseCode.OK, "Removed round Limit")
    self.rulesets[self.activeRuleset].roundLimit = limit
    return Response(ResponseCode.OK, f"Set round limit to {limit}")
  # End of setRoundLimit()

  def allowAliases(self, allow:bool) -> Response:
    """Sets whether or not the next session should scrape quotes with aliases of players, or just player names.
    Args:
      allow (bool): whether or not the next session should scrape quotes with aliases of players, or just player names.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    self.rulesets[self.activeRuleset].allowAliases = allow
    if allow:
      return Response(ResponseCode.OK, )
  # End of allowAliases()

  def setScrapeFrom(self, scrapeFrom:int|None) -> Response:
    """Sets the date and time to scrape dates from.
    Args:
      scrapeFrom (int | None): The Unix timestamp of the date and time to scrape from.  
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    if scrapeFrom == None:
      self.rulesets[self.activeRuleset].scrapeFrom = -1
      return Response(ResponseCode.OK, "Scraping from 0000-01-01 00:00:00")
    self.rulesets[self.activeRuleset].scrapeFrom = scrapeFrom
    return ResponseCode(ResponseCode.OK, f"Scraping from {dt.fromtimestamp(scrapeFrom).strftime('%Y-%m-%d %H:%M:%S')}.") 
  # End of setScrapeFrom()

  def setScrapeTo(self, scrapeTo:int|None) -> Response:
    """Sets the date and time to scrape dates from.
    Args:
      scrapeTo (int | None): The Unix timestamp of the date and time to scrape to.  
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    if scrapeTo == None:
      self.rulesets[self.activeRuleset].scrapeTo = -1
      return Response(ResponseCode.OK, "Scraping to 9999-12-31 23:59:59")
    self.rulesets[self.activeRuleset].scrapeTo = scrapeTo
    return ResponseCode(ResponseCode.OK, f"Scraping to {dt.fromtimestamp(scrapeTo).strftime('%Y-%m-%d %H:%M:%S')}.")
  # End of setScrapeTo()

  def setScrapeBetween(self, scrapeFrom:int|None, scrapeTo:int|None) -> Response:
    """Sets the dates and times to scrape dates between.
    Args:
      scrapeFrom (int | None): The Unix timestamp of the date and time to scrape from.  
      scrapeTo (int | None): The Unix timestamp of the date and time to scrape to.  
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    f = scrapeFrom(scrapeFrom)
    t = scrapeTo(scrapeTo)
    return Response(ResponseCode.OK, f + "\n" + t)
  # End of setScrapeBetween()
# End of SettingsManager