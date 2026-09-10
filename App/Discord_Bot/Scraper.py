## IMPORTS ##
from App.Helpers.Quote import Quote
from App.Helpers.Response import Response

QUOTE_LIMIT = 80

## CLASSES ##
class Scraper():
  """Handles scraping Discord channels for Quotes. 
  """
  ## PUBLIC METHODS ##
  @staticmethod
  def scrapeQuotes(channelID:str, scrapeFrom:int, scrapeTo:int, players:dict[str,list[str]]) -> list[Quote]:
    """Collects all the quotes in a channel between set dates.
    Args:
      channelID (str): The ID of the channel to collect quotes from.
      scrapeFrom (int): The UNIX timestamp to start scraping quotes from.
      scrapeTo (int): The UNIX timestamp to stop scraping quotes at.
    Returns:
      list[Quote]: The list of found quotes.
    """
    pass
  # End of scrapeQuotes()
# End of Scraper