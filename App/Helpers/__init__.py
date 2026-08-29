def stringifyArray(arr:list, delim:str=", ") -> str:
  """Creates a string showing all the values of an array.
  Params:
    arr (list): The array to stringify.
    delim (str): The delimiter to separate the strings by.
  Returns:
    str: The stringified array.
  """
  response = ""
  for val in arr[:-1]:
    response += str(val)
    response += delim
  response += arr[-1]
  return response
# End of stringifyArray()