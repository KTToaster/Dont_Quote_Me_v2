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
  def scrapeQuotes(channelID:str, scrapeFrom:int, scrapeTo:int) -> None:
    pass
  # End of scrapeQuotes()
  
  def storeQuote(quote:Quote) -> Response:
    pass
  # End of storeQuote()
# End of Scraper