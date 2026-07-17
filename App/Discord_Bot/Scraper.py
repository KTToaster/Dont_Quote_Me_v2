## IMPORTS ##
from App.Helpers.Quote import Quote
from App.Helpers.Response import Response

## CLASSES ##
class Scraper():
  """Handles scraping Discord channels for Quotes. 
  """

  ## CONSTRUCTOR ##
  def __init__(self):
    pass
  # End of __init__()  
  
  ## PUBLIC METHODS ##
  def scrapeQuotes(self, channelID:str, scrapeFrom:int, scrapeTo:int) -> None:
    """Collects all the quotes in a channel between set dates.
    Args:
      channelID (str): The ID of the channel to collect quotes from.
      scrapeFrom (int): The UNIX timestamp to start scraping quotes from.
      scrapeTo (int): The UNIX timestamp to stop scraping quotes at.
    """
    pass
  # End of scrapeQuotes()
  
  def storeQuote(self, quote:Quote) -> Response:
    """Stores a quote in the game's database.
    Args:
      quote (Quote): The quote object to store in the game's database.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    pass
  # End of storeQuote()
# End of Scraper