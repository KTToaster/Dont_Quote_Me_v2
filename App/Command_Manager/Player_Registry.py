## IMPORTS ##
from collections.abc import Callable

from App.Command_Manager.Parser import Parser
from App.Game_Manager.PlayerManager import PlayerManager
from App.Helpers.Response import Response, Status

## STATIC METHODS ##
def _createPlayer(players:PlayerManager, args:list[str]) -> Response:
  """Registers the `PlayerManager.createPlayer()` command.
  Args:
    players (PlayerManager): The PlayerManager that invokes the command.
    args (list[str]): The user's message in tokenised form, indicating the name to pass into the function.
  Returns:
    Response: A response consisting of a operation status code and a message that can be returned to the user.
  """
  try:
    name = args[0]
  except:
    return Response(Status.BAD_REQUEST, "No Name Given.")  
  return players.createPlayer(name)
# End of _createPlayer()

def _createAlias(players:PlayerManager, args:list[str]) -> list[Response]:
  """Registers the `PlayerManager.createAlias()` command.
  Args:
    players (PlayerManager): The PlayerManager that invokes the command.
    args (list[str]): The user's message in tokenised form, indicating the name, aliases and flags to pass into the function.
  Returns:
    Response: A response consisting of a operation status code and a message that can be returned to the user.
  """
  try:
    name, aliases, flags = Parser.paarseNameAliasesAndFlags(args)
  except SyntaxError as e:
    return Response(Status.BAD_REQUEST, e.msg)
  
  responses:list[Response] = []
  for alias in aliases:
    responses.append(players.createAlias(name, alias, flags))
  return responses
# End of _createAlias()

def _addPlayer(players:PlayerManager, args:list[str]) -> Response:
  """Registers the `PlayerManager.addPlayer()` command.
  Args:
    players (PlayerManager): The PlayerManager that invokes the command.
    args (list[str]): The user's message in tokenised form, indicating the name and flags to pass into the function.
  Returns:
    Response: A response consisting of a operation status code and a message that can be returned to the user.
  """
  try:
    name, flags = Parser.paarseNameAndFlags(args)
  except SyntaxError as e:
    return Response(Status.BAD_REQUEST, e.msg)
  return players.addPlayer(name, flags)          
# End of _addPlayer()

def _deletePlayer(players:PlayerManager, args:list[str]) -> Response:
  """Registers the `PlayerManager.deletePlayer()` command.
  Args:
    players (PlayerManager): The PlayerManager that invokes the command.
    args (list[str]): The user's message in tokenised form, indicating the name and flags to pass into the function.
  Returns:
    Response: A response consisting of a operation status code and a message that can be returned to the user.
  """
  try:
    name, flags = Parser.paarseNameAndFlags(args)
  except SyntaxError as e:
    return Response(Status.BAD_REQUEST, e.msg)
  return players.deletePlayer(name, flags)
# End of _deletePlayer()

def _deleteAlias(players:PlayerManager, args:list[str]) -> Response:
  """Registers the `PlayerManager.deleteAlias()` command.
  Args:
    players (PlayerManager): The PlayerManager that invokes the command.
    args (list[str]): The user's message in tokenised form, indicating the alias and flags to pass into the function.
  Returns:
    Response: A response consisting of a operation status code and a message that can be returned to the user.
  """
  try:
    name, flags = Parser.paarseNameAndFlags(args)
  except SyntaxError as e:
    return Response(Status.BAD_REQUEST, e.msg)
  return players.deleteAlias(name, flags)
# End of _deleteAlias()

def _removePlayer(players:PlayerManager, args:list[str]) -> Response:
  """Registers the `PlayerManager.removePlayer()` command.
  Args:
    players (PlayerManager): The PlayerManager that invokes the command.
    args (list[str]): The user's message in tokenised form, indicating the alias and flags to pass into the function.
  Returns:
    Response: A response consisting of a operation status code and a message that can be returned to the user.
  """
  try:
    name, flags = Parser.paarseNameAndFlags(args)
  except SyntaxError as e:
    return Response(Status.BAD_REQUEST, e.msg)
  return players.removePlayer(name, flags)
# End of _removePlayer()

def _listPlayers(players:PlayerManager, args:list[str]) -> Response:
  """Registers the `PlayerManager.listPlayers()` command.
  Args:
    players (PlayerManager): The PlayerManager that invokes the command.
    args (list[str]): The user's message in tokenised form.
  Returns:
    Response: A response consisting of a operation status code and a message that can be returned to the user.
  """
  return players.listPlayers()
# End of _listPlayers() 

def _listActive(players:PlayerManager, args:list[str]) -> Response:
  """Registers the `PlayerManager.listActive()` command.
  Args:
    players (PlayerManager): The PlayerManager that invokes the command.
    args (list[str]): The user's message in tokenised form.
  Returns:
    Response: A response consisting of a operation status code and a message that can be returned to the user.
  """
  return players.listActivePlayers()
# End of _listActive()

def _inspectPlayer(players:PlayerManager, args:list[str]) -> Response:
  """Registers the `PlayerManager.inspectPlayer()` command.
  Args:
    players (PlayerManager): The PlayerManager that invokes the command.
    args (list[str]): The user's message in tokenised form, indicating the name and flags to pass into the function.
  Returns:
    Response: A response consisting of a operation status code and a message that can be returned to the user.
  """
  try:
    name, flags = Parser.paarseNameAndFlags(args)
  except SyntaxError as e:
    return Response(Status.BAD_REQUEST, e.msg)
  return players.inspectPlayer(name, flags)
# End of _inspectPlayer()

## CONSTANTS ##
PLAYER_REGISTER: dict[str,Callable[[PlayerManager, list[str]], Response|list[Response]]] = {
  "/createplayer":_createPlayer,
  "/createalias":_createAlias,
  "/addplayer":_addPlayer,
  "/deleteplayer":_deletePlayer,
  "/deletealias":_deleteAlias,
  "/removeplayer":_removePlayer,
  "/listplayers":_listPlayers,
  "/listactive":_listActive,
  "/inspectplayer":_inspectPlayer,
}