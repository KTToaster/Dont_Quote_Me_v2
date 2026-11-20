## IMPORTS ##
from collections.abc import Callable

from App.Command_Manager.Parser import Parser
from App.Game_Manager.SettingsManager import SettingsManager
from App.Helpers.Response import Response, ResponseCode

## STATIC METHODS ##
def _quoteChannel(settings:SettingsManager, args:list[str]) -> Response:
  try:
    channel = args[0]
    # TODO: Validate channel
  except:
    return Response(ResponseCode.BAD_REQUEST, "No Channel Given.")
  return settings.setQuoteChannel(channel)
# End of _quoteChannel()

def _roundLimit(settings:SettingsManager, args:list[str]) -> Response:
  try:
    limit = Parser.parseNumber(args)
  except SyntaxError as e:
    return Response(ResponseCode.BAD_REQUEST, e.msg)  
  return settings.setRoundLimit(limit)
# End of _roundLimit()

def _allowAliases(settings:SettingsManager, args:list[str]) -> Response:
  try:
    allow = Parser.parseBoolean(args)
  except SyntaxError as e:
    return Response(ResponseCode.BAD_REQUEST, e.msg)
  return settings.allowAliases(allow)
# End of _allowAliases()

def _scrapeFrom(settings:SettingsManager, args:list[str]) -> Response:
  try:
    timestamp = Parser.parseDateTime(args)
  except SyntaxError as e:
    return Response(ResponseCode.BAD_REQUEST, e.msg)
  return settings.setScrapeFrom(timestamp)
# End of _scrapeFrom()

def _scrapeTo(settings:SettingsManager, args:list[str]) -> Response:
  try:
    timestamp = Parser.parseDateTime(args)
  except SyntaxError as e:
    return Response(ResponseCode.BAD_REQUEST, e.msg)
  return settings.setScrapeTo(timestamp)
# End of _scrapeTo()

def _scrapeBetween(settings:SettingsManager, args:list[str]) -> Response:
  f:int; t:int
  try:
    if len(args) == 2:
      f = Parser.parseDateTime([args[0]])
      t = Parser.parseDateTime([args[1]])
    elif len(args) >= 4:
      f = Parser.parseDateTime(args[0:1])
      t = Parser.parseDateTime(args[2:3])
    else:
      return Response(ResponseCode.BAD_REQUEST, "Ambiguous datetimes given.")
  except SyntaxError as e:
    return Response(ResponseCode.BAD_REQUEST, e.msg)
  return settings.setScrapeBetween(f, t)
# End of _scrapeBetween()

def _saveRuleset(settings:SettingsManager, args:list[str]) -> Response:
  try:
    name = args[0]
  except:
    return Response(ResponseCode.BAD_REQUEST, "No name Given.")
  return settings.saveRuleset(name)
# End of _saveRuleset()

def _loadRuleset(settings:SettingsManager, args:list[str]) -> Response:
  try:
    name = args[0]
  except:
    return Response(ResponseCode.BAD_REQUEST, "No name Given.")
  return settings.loadRuleset(name)
# End of _loadRuleset()

def _deleteRuleset(settings:SettingsManager, args:list[str]) -> Response:
  try:
    name, flags = Parser.parseNameAndFlags(args)
  except SyntaxError as e:
    return Response(ResponseCode.BAD_REQUEST, e.msg)
  return settings.deleteRuleset(name, flags)
# End of _deleteRuleset()

def _listRulesets(settings:SettingsManager, args:list[str]) -> Response:
  return settings.listRulesets()
# End of _listRulesets()

def _inspectRuleset(settings:SettingsManager, args:list[str]) -> Response:
  try:
    name, flags = Parser.parseNameAndFlags(args)
  except SyntaxError as e:
    return Response(ResponseCode.BAD_REQUEST, e.msg)
  return settings.inspectRuleset(name, flags)
# End of _inspectRuleset()

## CONSTANTS ##
SETTINGS_REGISTER: dict[str,Callable[[SettingsManager, list[str]], Response]] = {
  "/quotechannel":_quoteChannel,
  "/roundlimit":_roundLimit,
  "/allowaliases":_allowAliases,
  "/scrapefrom":_scrapeFrom,
  "/scrapeto":_scrapeTo,
  "/scrapebetween":_scrapeBetween,
  "/saveruleset":_saveRuleset,
  "/loadruleset":_loadRuleset,
  "/deleteruleset":_deleteRuleset,
  "/listrulesets":_listRulesets,
  "/inspectruleset":_inspectRuleset,
}