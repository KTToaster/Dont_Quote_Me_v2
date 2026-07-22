## IMPORTS ##
from discord.message import Message
from discord.channel import TextChannel

from App.Discord_Bot.Scraper import Scraper
from App.Game_Manager.SettingsManager import SettingsManager
from App.Helpers.Response import *
from App.Game_Manager.PlayerManager import PlayerManager
from App.Game_Manager.StateManager import StateManager

## GLOBALS ##

## CLASSES ##
class Client():
  """Handles communication for a specific guild/Discord server.
  """
  ## VALUES ##
  ID:str                    # The ID of the guild that is being communicated with
  players:PlayerManager     # The object that handles the players for this guild.
  settings:SettingsManager  # The object that handles the settings for this guild.
  state:StateManager        # The object that handles the game state for this guild.
  scraper:Scraper           # The object that can scrape this guild.
  lastActivity:int          # The last time the guild was communicated with. 
  gameIndex:int             # Counts the number of games that have been played by this client.
  
  ## CONSTRUCTOR ##
  def __init__(self):
    pass
  # End of __init__()
  
  
  ## PUBLIC METHODS ##
  async def on_message(self, message:Message) -> None:
    """Handles a message being sent to the discord server associated with this client.
    Args:
      message (Message): The message that has been sent to the client.
    """
    # Get commands and params
    tokenisedMessage = message.content.split(" ")[1:]
    if(len(tokenisedMessage) == 0):
      self.sendMessage(message.channel, self.__help())
      return
    
    # Match commands to their respective functions.
    match(tokenisedMessage[0].lower):
      case "/createplayer":     # Player Commands
        self.sendMessage(message.channel, self.players.createPlayer(tokenisedMessage[1:]))
        return
      case "/createalias":
        self.sendMessage(message.channel, self.players.createAlias(tokenisedMessage[1:]))
        return
      case "/addplayer":
        self.sendMessage(message.channel, self.players.addPlayer(tokenisedMessage[1:]))
        return
      case "/deleteplayer":
        self.sendMessage(message.channel, self.players.deletePlayer(tokenisedMessage[1:]))
        return
      case "/deletealias":
        self.sendMessage(message.channel, self.players.deleteAlias(tokenisedMessage[1:]))
        return
      case "/listplayers":
        self.sendMessage(message.channel, self.players.listPlayers(tokenisedMessage[1:]))
        return
      case "/listactive":
        self.sendMessage(message.channel, self.players.listActivePlayers(tokenisedMessage[1:]))
        return
      case "/inspectplayer":
        self.sendMessage(message.channel, self.players.playerDetails(tokenisedMessage[1:]))
        return
      case "/set":              # Settings Commands
        self.sendMessage(message.channel, self.settings.setRule(tokenisedMessage[1:]))
        return
      case "/saveruleset":
        self.sendMessage(message.channel, self.settings.saveRuleset(tokenisedMessage[1:]))
        return
      case "/loadruleset":
        self.sendMessage(message.channel, self.settings.loadRuleset(tokenisedMessage[1:]))
        return
      case "/deleteruleset":
        self.sendMessage(message.channel, self.settings.deleteRuleset(tokenisedMessage[1:]))
        return
      case "/start" | "/next":  # State Commands
        self.sendMessage(message.channel, self.state.nextRound())
        return
      case "/end":
        self.sendMessage(message.channel, self.state.endGame())
        return
      case "/help":             # Help Commands
        self.sendMessage(message.channel, self.__help(tokenisedMessage[1:]))
        return
      case _:
        self.sendMessage(message.channel, Response(ResponseCode.BAD_COMMAND, f"""Unknown command \"{tokenisedMessage[0]}\".
                         Use \"/help\" for a list of all commands."""))
  # End of on_message()

  async def sendMessage(self, channel:TextChannel, message:Response) -> None:
    """Sends a message to the discord guid associated with this client. 
    Args:
      channel (TextChannel): The channel to send the message to.
      message (Response): The message to send to the channel.
    """
    channel.send(message.message)
  # End of sendMessage()
  
  ## PRIVATE METHODS ##
  def __help(self, params:list[str]|None=None) -> Response:
    """Responds to a /help command
    Args:
      params (list[str] | None): A string broken into tokens indicating the parameters of the command. Defaults to None.
      Can include the command to get help for. Check Docs/command_grammar.md for full details.
    """
    paramCount = 0
    try:
      paramCount = len(params)
    except TypeError:
      return HELPDEFAULT
    if(paramCount == 0):
      return HELPDEFAULT
    elif(paramCount == 1):
      match(params[0].lower()):
        case "players":
          return HELPPLAYERS
        case "settings":
          return HELPSETTINGS
        case "state" | "play":
          return HELPSTATE
        case _:
          return Response(ResponseCode.BAD_PARAMETERS, f"""Invalid parameter {params[0]}.
          Use \"/help\" for a list of all commands.""")
    else:
      return Response(ResponseCode.BAD_PARAMETERS, f"""Invalid number of parameters. Expected 0 or 1, received: {paramCount}.""")
  # End of help()
# End of Client