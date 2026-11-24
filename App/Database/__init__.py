## IMPORTS ##
from os import getenv
from typing import Any, Sequence
from dotenv import load_dotenv
import mysql.connector as sql
from mysql.connector.abstracts import MySQLCursorAbstract
from mysql.connector.types import MySQLConvertibleType

## CONSTANTS ##
HOST = "127.0.0.1"  # Local for testing
USER = "root"
PORT = 3306 
DATABASE = "dontquotemeDB"

CONNECTION_DETAILS = {
  "user":USER,
  "host": HOST,
  "port": PORT,
  "database":DATABASE,
}

## CLASSES ##
class Database:
  @staticmethod
  def fetchAll(query:str, params:Sequence[MySQLConvertibleType] | dict[str, MySQLConvertibleType] = (), map_results:bool = False) -> list[tuple[Any]]:
    """Wrapper function for `MySQLCursorAbstract.fetchall()` that handles the full connection and execution cycle for the dontquotemeDB.
    Args:
      query (str): The Operation to be executed - it can be a single or a multi statement.
      params (Sequence[MySQLConvertibleType] | dict[MySQLConvertibleType], optional): The parameters found in the tuple or dictionary params are bound to the variables in the operation. Specify variables using `%s` or `%(name)s` parameter style (that is, using format or pyformat style). Defaults to ().
      map_results (bool, optional): If True, it allows you to know what statement caused what result set. Only relevant when working with multi statements. Defaults to False.
    Returns:
      list[tuple[Any]]: The rows returned by query.
    """
    conn = sql.connect(**CONNECTION_DETAILS, passwd=Database.__loadPassword())
    try:
      cursor = conn.cursor()
      try:  
        cursor.execute(query, params, map_results)
        return cursor.fetchall()
      finally:
        cursor.close()
    finally:
      conn.close()
  # End of fetchAll() 

  @staticmethod
  def fetchOne(query:str, params:Sequence[MySQLConvertibleType] | dict[str, MySQLConvertibleType] = (), map_results:bool = False) -> tuple[Any]:
    """Wrapper function for `MySQLCursorAbstract.fetchone()` that handles the full connection and execution cycle for the dontquotemeDB.
    Args:
      query (str): The Operation to be executed - it can be a single or a multi statement.
      params (Sequence[MySQLConvertibleType] | dict[MySQLConvertibleType], optional): The parameters found in the tuple or dictionary params are bound to the variables in the operation. Specify variables using `%s` or `%(name)s` parameter style (that is, using format or pyformat style). Defaults to ().
      map_results (bool, optional): If True, it allows you to know what statement caused what result set. Only relevant when working with multi statements. Defaults to False.
    Returns:
      tuple[Any]: The row returned by query.
    """
    conn = sql.connect(**CONNECTION_DETAILS, passwd=Database.__loadPassword())
    try:
      cursor = conn.cursor()
      try:  
        cursor.execute(query, params, map_results)
        return cursor.fetchone()
      finally:
        cursor.close()
    finally:
      conn.close()
  # End of fetchOne()

  @staticmethod
  def fetchMany(query:str, params:Sequence[MySQLConvertibleType] | dict[str, MySQLConvertibleType] = (), map_results:bool = False, size:int=1) -> list[tuple[Any]]:
    """Wrapper function for `MySQLCursorAbstract.fetchmany()` that handles the full connection and execution cycle for the dontquotemeDB.
    Args:
      query (str): The Operation to be executed - it can be a single or a multi statement.
      params (Sequence[MySQLConvertibleType] | dict[MySQLConvertibleType], optional): The parameters found in the tuple or dictionary params are bound to the variables in the operation. Specify variables using `%s` or `%(name)s` parameter style (that is, using format or pyformat style). Defaults to ().
      map_results (bool, optional): If True, it allows you to know what statement caused what result set. Only relevant when working with multi statements. Defaults to False.
    Returns:
      list[tuple[Any]]: The rows returned by query.
    """
    conn = sql.connect(**CONNECTION_DETAILS, passwd=Database.__loadPassword())
    try:
      cursor = conn.cursor()
      try:  
        cursor.execute(query, params, map_results)
        return cursor.fetchmany(size)
      finally:
        cursor.close()
    finally:
      conn.close()
  # End of fetchMany()

  @staticmethod
  def execute(query:str, params:Sequence[MySQLConvertibleType]|dict[str, MySQLConvertibleType]=(), map_results:bool=False, commit:bool=True) -> int:
    """Wrapper function for `MySQLCursorAbstract.execute()` and `(PooledMySQLConnection | MySQLConnectionAbstract).commit()` that handles the full connection and execution cycle for the dontquotemeDB.
    Args:
      query (str): The Operation to be executed - it can be a single or a multi statement.
      params (Sequence[MySQLConvertibleType] | dict[MySQLConvertibleType], optional): The parameters found in the tuple or dictionary params are bound to the variables in the operation. Specify variables using `%s` or `%(name)s` parameter style (that is, using format or pyformat style). Defaults to ().
      map_results (bool, optional): If True, it allows you to know what statement caused what result set. Only relevant when working with multi statements. Defaults to False.
      commit (bool): Whether or not to commit the changes. If False, the changes will be staged but not executed. Defaults to True. 
    Returns:
      int: The number of rows affected by the query.
    """
    conn = sql.connect(**CONNECTION_DETAILS, passwd=Database.__loadPassword())
    try:
      cursor = conn.cursor()
      try:  
        cursor.execute(query, params, map_results)
        if(commit):
          conn.commit()
        return cursor.rowcount
      finally:
        cursor.close()
    finally:
      conn.close()
  # End of execute()

  @staticmethod
  def executeMany(query:str, params:Sequence[Sequence[MySQLConvertibleType] | dict[str, MySQLConvertibleType]], commit:bool=True) -> int:
    """Wrapper function for `MySQLCursorAbstract.executemany()` and `(PooledMySQLConnection | MySQLConnectionAbstract).commit()` that handles the full connection and execution cycle for the dontquotemeDB.
    Args:
      query: Operation to be executed.
      params: Parameters to be used when executing the operation.
      commit (bool): Whether or not to commit the changes. If False, the changes will be staged but not executed. Defaults to True. 
    Returns:
      int: The number of rows affected by the query.
    """
    conn = sql.connect(**CONNECTION_DETAILS, passwd=Database.__loadPassword())
    try:
      cursor = conn.cursor()
      try:  
        cursor.executemany(query, params)
        if(commit):
          conn.commit()
        return cursor.rowcount
      finally:
        cursor.close()
    finally:
      conn.close()
  # End of execute()

  ## PRIVATE METHODS ##
  @staticmethod
  def __loadPassword() -> str:
    """Loads the database's password from the environment file. 
    Raises:
      NameError: Raised when the Environment Variable cannot be found.
      FileNotFoundError: Raised when the Environment File cannot be found.
    Returns:
      str: The database's password.
    """
    if load_dotenv():
      password = getenv("DB_PASSWORD")
      if password == None:
        raise NameError("DB_PASSWORD not found in .env file.")
      return password
    raise FileNotFoundError("Could not find .env file.")  
  # End of __loadPassword()
# End of Database