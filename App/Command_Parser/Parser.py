from App.Command_Parser import *
from App.Helpers.Response import Response

class Parser():
  @staticmethod
  def parseName(params:list[str]) -> str:
    if len(params) < 1:
      raise TypeError("No name given.")
    return params[0]
  # End of parseName()

  @staticmethod
  def parseNameAndAliases(params:list[str]) -> tuple[str, set[str]]:
    if len(params) < 1:
      raise TypeError("No name given.")
    if len(params) < 1:
      raise TypeError("No alias given.")

    return params[0], set(params[1:])
  # End of parseNameAndAliases()

  @staticmethod
  def parseNameAndFlags(params:list[str]) -> tuple[str, set[str]]:
    if len(params) < 1:
      raise TypeError("No name given.")
    
    flags = set()
    for param in params[1:]:
      if len(flags) > 0:
        if param in FLAG_MAP:
          flags.add(FLAG_MAP[param])
        else:
          break
      elif param in FLAG_MAP:
        flags.add(FLAG_MAP[param])
    
    return params[0], flags
  # End of parseNameAndFlags()

  @staticmethod
  def parseNameAliasesAndFlags(params:list[str]) -> tuple[str, set[str], set[str]]:
    if len(params) < 1:
      raise TypeError("No name given.")

    aliases = set()
    flags = set()
    for param in params[1:]:
      if len(flags) > 0:
        if param in FLAG_MAP:
          flags.add(FLAG_MAP[param])
        else:
          break
      elif param in FLAG_MAP:
        flags.add(FLAG_MAP[param])
      else:
        aliases.add(param)

    if len(aliases) < 1:
      raise TypeError("No alias given.")

    return params[0], aliases, flags
  # End of parseNameAliasesAndFlags()

  @staticmethod
  def parseNumber(params:list[str]) -> int:
    pass
  # End of parseNumber()

  @staticmethod
  def parseDateTime(params:list[str]) -> int:
    pass
  # End of parseDateTime()

  @staticmethod
  def parseDateTimes(params:list[str]) -> int:
    pass
  # End of parseDateTime()

  @staticmethod
  def parseBoolean(params:list[str]) -> bool:
    pass
  # End of parseBoolean()