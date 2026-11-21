## IMPORTS ##
from collections.abc import Callable

from App.Command_Manager.Parser import Parser
from App.Game_Manager.PlayerManager import PlayerManager
from App.Helpers.Response import Response, ResponseCode

## STATIC METHODS ##
def _createPlayer(players:PlayerManager, args:list[str]) -> Response:
  try:
    name = args[0]
  except:
    return Response(ResponseCode.BAD_REQUEST, "No Name Given.")  
  return players.createPlayer(name)
# End of _createPlayer()

def _createAlias(players:PlayerManager, args:list[str]) -> list[Response]:
  try:
    name, aliases, flags = Parser.parseNameAliasesAndFlags(args)
  except SyntaxError as e:
    return Response(ResponseCode.BAD_REQUEST, e.msg)
  
  responses:list[Response] = []
  for alias in aliases:
    responses.append(players.createAlias(name, alias, flags))
  return responses
# End of _createAlias()

def _addPlayer(players:PlayerManager, args:list[str]) -> Response:
  try:
    name, flags = Parser.parseNameAndFlags(args)
  except SyntaxError as e:
    return Response(ResponseCode.BAD_REQUEST, e.msg)
  return players.addPlayer(name, flags)          
# End of _addPlayer()

def _deletePlayer(players:PlayerManager, args:list[str]) -> Response:
  try:
    name, flags = Parser.parseNameAndFlags(args)
  except SyntaxError as e:
    return Response(ResponseCode.BAD_REQUEST, e.msg)
  return players.deletePlayer(name, flags)
# End of _deletePlayer()

def _deleteAlias(players:PlayerManager, args:list[str]) -> Response:
  try:
    name, flags = Parser.parseNameAndFlags(args)
  except SyntaxError as e:
    return Response(ResponseCode.BAD_REQUEST, e.msg)
  return players.deleteAlias(name, flags)
# End of _deleteAlias()

def _removePlayer(players:PlayerManager, args:list[str]) -> Response:
  try:
    name, flags = Parser.parseNameAndFlags(args)
  except SyntaxError as e:
    return Response(ResponseCode.BAD_REQUEST, e.msg)
  return players.removePlayer(name, flags)
# End of _removePlayer()

def _listPlayers(players:PlayerManager, args:list[str]) -> Response:
  return players.listPlayers()
# End of _listPlayers() 

def _listActive(players:PlayerManager, args:list[str]) -> Response:
  return players.listActivePlayers()
# End of _listActive()

def _inspectPlayer(players:PlayerManager, args:list[str]) -> Response:
  try:
    name, flags = Parser.parseNameAndFlags(args)
  except SyntaxError as e:
    return Response(ResponseCode.BAD_REQUEST, e.msg)
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