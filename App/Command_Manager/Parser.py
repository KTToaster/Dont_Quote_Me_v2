from App.Command_Manager import *
from App.Helpers.Response import Response

class Parser():
  @staticmethod
  def parseNameAndAliases(args:list[str]) -> tuple[str, set[str]]:
    if len(args) < 1:
      raise SyntaxError("No name given.")
    if len(args) < 2:
      raise SyntaxError("No alias given.")

    return args[0], set(args[1:])
  # End of parseNameAndAliases()

  @staticmethod
  def parseNameAndFlags(args:list[str]) -> tuple[str, set[str]]:
    if len(args) < 1:
      raise SyntaxError("No name given.")
    
    flags = set()
    for param in args[1:]:
      if len(flags) > 0:
        if param in FLAG_MAP:
          flags.add(FLAG_MAP[param])
        else:
          break
      elif param in FLAG_MAP:
        flags.add(FLAG_MAP[param])
    
    return args[0], flags
  # End of parseNameAndFlags()

  @staticmethod
  def parseNameAliasesAndFlags(args:list[str]) -> tuple[str, set[str], set[str]]:
    if len(args) < 1:
      raise SyntaxError("No name given.")

    aliases = set()
    flags = set()
    for param in args[1:]:
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
      raise SyntaxError("No alias given.")

    return args[0], aliases, flags
  # End of parseNameAliasesAndFlags()

  @staticmethod
  def parseNumber(args:list[str]) -> int:
    if len(args) < 1:
      return -1
    if args[0].isdigit():
      return int(args[0])
    raise SyntaxError("Argument is not a number.")
  # End of parseNumber()

  @staticmethod
  def parseDateTime(args:list[str]) -> int:
    pass
  # End of parseDateTime()

  @staticmethod
  def parseBoolean(args:list[str]) -> bool:
    if len(args) < 1 or args[0] in TRUE_KEYWORDS:
      return True
    elif args[0] in FALSE_KEYWORDS:
      return False
    raise SyntaxError("Argument is not a boolean expression.")
  # End of parseBoolean()