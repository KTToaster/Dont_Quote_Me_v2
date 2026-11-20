## IMPORTS ##
from App.Command_Manager.Player_Registry import *

## CONSTANTS ##
TRUE_KEYWORDS = {"true", "on", "y", "yes", "t"}
FALSE_KEYWORDS = {"false", "off", "n", "no", "f"}

FLAG_MAP = {
  "-f":"force",
  "--force":"force",
  "-s":"strict",
  "--strict":"strict",
  "-r":"raw",
  "--raw":"raw"
}