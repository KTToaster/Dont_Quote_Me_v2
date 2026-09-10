## IMPORTS ##
from App.Discord_Bot.Scraper import Scraper
from App.Game_Manager.SettingsManager import Ruleset
from App.Helpers.Quote import Quote
from App.Helpers.Response import Response, ResponseCode

from random import randint
from datetime import datetime
from time import strftime

## CLASSES ##
class StateManager():
  """Handles the game state of the current DQM game.
  """
  ## VALUES ##
  lastQuote:Quote|None          # The last quote that was used in the game
  availableQuotes:list[Quote]   # The quotes that can be used in the rounds.
  ruleset:Ruleset               # The rules that the game has to follow.
  players:dict[str, list[str]]  # The players that can be quoted.
  roundNumber:int               # The round number the game is on.
  newest:int                    # The timestamp of the most recent quote.

  ## CONSTRUCTOR ##
  def __init__(self, ruleset:Ruleset, players:dict[str,list[str]]):
    self.lastQuote = None
    self.ruleset = ruleset
    self.players = players
    self.roundNumber = 0

    self.availableQuotes = Scraper.scrapeQuotes(ruleset.quotesChannel, 
                                                ruleset.scrapeFrom, 
                                                ruleset.scrapeTo,
                                                players)
    
    self.newest = self.availableQuotes[-1].sent
  # End of __init__()
  
  ## PUBLIC METHODS ##
  def nextRound(self) -> Response:
    """Runs the next round of the current game.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    lastDetails = self.__lastQuoteToString()

    if(self.roundNumber > self.ruleset.roundLimit):
      return Response(ResponseCode.REDIR_END, "Round limit reached.\n")
    self.roundNumber += 1

    if(len(self.availableQuotes) == 0):
      # Try to get more quotes
      self.availableQuotes = Scraper.scrapeQuotes(self.ruleset.quotesChannel,
                                                  self.newest, 
                                                  self.ruleset.scrapeTo,
                                                  self.players)
      if(len(self.availableQuotes) == 0):
        return Response(ResponseCode.REDIR_END, "No more available quotes.\n")

    # Print this round's quote
    quoteNum = randint(0, len(self.availableQuotes)-1)
    self.lastQuote = self.availableQuotes[quoteNum]
    self.availableQuotes.pop(quoteNum)
    return Response(ResponseCode.OK, lastDetails+f"*Round {self.roundNumber}*\n{self.lastQuote.quote}")
  # End of nextRound()
  
  def endGame(self) -> Response:
    """Ends the current game, resetting the available quotes.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    return(ResponseCode.OK, "Game Over. Thank you for playing.")
  # End of endGame()

  ## PRIVATE METHODS ##
  def __lastQuoteToString(self) -> str:
    """Prints the details of the last quote as a formatted string.
    Returns:
      str: The formatted string constructed from the last quote's details.
    """
    lastDetails = ""
    if(self.lastQuote != None):
      lastDetails += "Player: " + self.lastQuote.quoted + "\n"
      if(self.lastQuote.context != None):
        lastDetails += "Context: " + self.lastQuote.context + "\n"
      lastDetails += "Sent: " + datetime.fromtimestamp(self.lastQuote.sent).strftime('%Y-%m-%d %H:%M:%S') + "\n\n"
    return lastDetails
  # End of __fetchQuotes()
# End of StateManager