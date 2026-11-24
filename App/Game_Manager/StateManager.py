## IMPORTS ##
from App.Discord_Bot.Scraper import Scraper
from App.Game_Manager.SettingsManager import Ruleset
from App.Helpers.Quote import Quote
from App.Helpers.Response import Response, Status

from random import randint
from datetime import datetime

## CLASSES ##
class StateManager():
  """Handles the game state of the current DQM game.
  """
  ## VALUES ##
  lastQuote:Quote|None        # The last quote that was used in the game
  settings:Ruleset            # The rules that the game has to follow.
  players:dict[str,set[str]]  # The players that can be quoted.
  roundNumber:int             # The round number the game is on.
  scraper:Scraper             # The scraper attached to this object.

  ## CONSTRUCTOR ##
  def __init__(self, guild_id:int, settings:Ruleset, players:dict[str,set[str]]):
    self.lastQuote = None
    self.settings = settings
    self.players = players
    self.roundNumber = 0
    self.scraper = Scraper(guild_id)
    # TODO: check if there are quotes in the NoSQL DB before scraping new ones.
    self.scraper.scrapeQuotes(self.settings, self.players)
  # End of __init__()
  
  ## PUBLIC METHODS ##
  def play(self) -> Response:
    """Runs the next round of the current game.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    if(self.settings.quotesChannel == None):
      return Response(Status.FAILED_DEPENDENCY, "Cannot get quotes as the Quote Channel is undefined. Use /help settings for more information.")

    self.roundNumber += 1
    if self.roundNumber > self.settings.roundLimit:
      return self.endGame()
    
    return Response(Status.OK, self.__lastQuoteToString() + f"Round {self.roundNumber}:\n\"" + self.lastQuote.quote + "\"")
  # End of nextRound()
  
  def endGame(self) -> Response:
    """Ends the current game, resetting the available quotes.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    Scraper.clearQuotes()
    return Response(Status.OK, self.__lastQuoteToString() + "Game Over. Thank you for playing.")
  # End of endGame()

  ## PRIVATE METHODS ##
  def __lastQuoteToString(self) -> str:
    """Prints the details of the last quote as a formatted string.
    Returns:
      str: The formatted string constructed from the last quote's details.
    """
    lastDetails = ""
    if self.lastQuote != None:
      lastDetails += "Player: " + self.lastQuote.quoted + "\n"
      if self.lastQuote.context != None:
        lastDetails += "Context: " + self.lastQuote.context + "\n"
      lastDetails += "Sent: " + datetime.fromtimestamp(self.lastQuote.sent).strftime('%Y-%m-%d %H:%M:%S') + "\n\n"
    return lastDetails
  # End of __fetchQuotes()
# End of StateManager