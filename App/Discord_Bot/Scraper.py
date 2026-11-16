## IMPORTS ##
from App.Game_Manager.SettingsManager import Ruleset
from App.Helpers.Quote import Quote
from App.Helpers.Response import Response

QUOTE_LIMIT = 80

## CLASSES ##
class Scraper():
  """Handles scraping Discord channels for Quotes. 
  """
  ## PUBLIC METHODS ##
  @staticmethod
  def scrapeQuotes(settings:Ruleset, players:dict[str,list[str]]) -> list[Quote]:
    """Collects all the quotes in a channel between set dates.
    Args:
      settings (Ruleset): The settings the scraper should follow when scraping quotes
      players (dict[str,set[str]]): 
    Returns:
      list[Quote]: The list of found quotes.
    """
    pass
  # End of scrapeQuotes()
# End of Scraper