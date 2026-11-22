## IMPORTS ##
from App.Game_Manager.SettingsManager import Ruleset
from App.Helpers.Quote import Quote
from App.Helpers.Response import Response

## CLASSES ##
class Scraper():
  """Handles scraping Discord channels for Quotes. 
  """
  ## VALUES ##
  GUILD_ID:int  # The ID of the guild to scrape quotes from.
  
  ## CONSTRUCTOR ##
  def __init__(self, GUILD_ID:int):
    self.GUILD_ID = GUILD_ID
  # End of __init__()

  ## PUBLIC METHODS ##
  def scrapeQuotes(self, settings:Ruleset, players:dict[str,list[str]]) -> None:
    """Collects all the valid quotes in a channel and stores them in a local NoSQL database.
    Args:
      settings (Ruleset): The settings the scraper should follow when scraping quotes
      players (dict[str,set[str]]): 
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
  # End of scrapeQuotes()

  def popQuote(self) -> Quote:
    """Fetches a quote from the NoSQL database and removes it.
    Returns:
      Quote: Quote returned from the database
      Response: A response code indicating an error, with a message that can be returned to the user.
    """ 
  # End of getQuote()

  def clearQuotes(self) -> None:
    """Removes all the remaining quotes in the NoSQL database.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
  # End of clearQuotes()
# End of Scraper