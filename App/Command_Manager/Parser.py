from App.Command_Manager import *

class Parser():
  @staticmethod
  def parseNameAndAliases(args:list[str]) -> tuple[str, set[str]]:
    """Parses the name of a player as the first argument, and subsequent arguments as aliases.
    Args:
      args (list[str]): The user's message in tokenised form, containing the Name and Aliases to parse.
    Raises:
      SyntaxError: The details could not be parsed due to incorrect syntax.
    Returns:
      tuple[str, set[str]]: The name parsed by the function; the aliases parsed by the function.
    """
    if len(args) < 1:
      raise SyntaxError("No name given.")
    if len(args) < 2:
      raise SyntaxError("No alias given.")

    return args[0], set(args[1:])
  # End of parseNameAndAliases()

  @staticmethod
  def parseNameAndFlags(args:list[str]) -> tuple[str, set[str]]:
    """Parses the name of a player as the first argument, and subsequent arguments beginning with '-' as flags.
    Stops parsing flags as soon as an invalid flag is found.
    Args:
      args (list[str]): The user's message in tokenised form, containing the Name and Aliases to parse.
    Raises:
      SyntaxError: The details could not be parsed due to incorrect syntax.
    Returns:
      tuple[str, set[str]]: The name parsed by the function; the flags parsed by the function.
    """
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
    """Parses the name of a player as the first argument, subsequent arguments as aliases or flags if they begin with '-'.
    Starts parsing arguments as flags when the first flag is found. Stops parsing flags as soon as an invalid flag is found.
    Args:
      args (list[str]): The user's message in tokenised form, containing the Name, Aliases and Flags to parse.
    Raises:
      SyntaxError: The details could not be parsed due to incorrect syntax.
    Returns:
      tuple[str, set[str], set[str]]: The name parsed by the function; the aliases parsed by the function; the flags parsed by the function.
    """
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
    """Parses a number.
    Args:
      args (list[str]): The user's message in tokenised form, containing the Number to parse.
    Raises: 
      SyntaxError: The details could not be parsed due to incorrect syntax.
    Returns:
      int: The number parsed by the function.
    """
    if len(args) < 1:
      return -1
    if args[0].isdigit():
      return int(args[0])
    raise SyntaxError("Argument is not a number.")
  # End of parseNumber()

  @staticmethod
  def parseDateTime(args:list[str]) -> int:
    """Parses a datetime into a UNIX timestamp.
    Args:
      args (list[str]): The user's message in tokenised form, containing the Datetime to parse.
    Raises:
      SyntaxError: The details could not be parsed due to incorrect syntax.
    Returns:
      int: The unix timestamp parsed by the function.
    """
    pass
  # End of parseDateTime()

  @staticmethod
  def parseBoolean(args:list[str]) -> bool:
    """Parses a boolean value.
    Args:
      args (list[str]): The user's message in tokenised form, containing the Boolean to parse.
      Treats no arguments as True.
    Raises:
      SyntaxError: The details could not be parsed due to incorrect syntax.
    Returns:
      bool: The boolean value parsed by the function.
    """
    if len(args) < 1 or args[0] in TRUE_KEYWORDS:
      return True
    elif args[0] in FALSE_KEYWORDS:
      return False
    raise SyntaxError("Argument is not a boolean expression.")
  # End of parseBoolean()
# End of Parser