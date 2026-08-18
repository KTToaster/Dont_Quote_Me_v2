## IMPORTS ##
from typing import List
import mysql.connector
from mysql.connector.types import RowType
from mysql.connector.cursor import MySQLCursor
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from os import getenv
from dotenv import load_dotenv

from App.Helpers.Response import Response, ResponseCode

## GLOBALS ##
HOST = "127.0.0.1"  # Local for testing
USER = "root"
PORT = 3306 
DATABASE = "dontquotemeDB"
password:str
connection: PooledMySQLConnection | MySQLConnectionAbstract

## CLASSES ##
class Database():
  """Handles Communication between the DQM Game and it's database
  """
  ## PUBLIC METHODS ##
  @staticmethod
  def connect() -> Response:
    if(password):
      return(ResponseCode.NOT_MODIFIED)
    print(Database.__load_password().message)

    global connection
    connection = mysql.connector.connect(
      user = USER,
      host = HOST,
      port=PORT,
      database = DATABASE,
      passwd = password
    )
    
  # End of connect()
  
  @staticmethod
  def disconnect() -> Response:
    global connection
    connection.disconnect()
  # End of disconnect()

  @staticmethod
  def selectQuery(query:str) -> tuple[Response, List[RowType]]:
    """Sends a select query to the MySQL Database.
    Args:
      query (str): The query to send to the database.
    Returns:
      Response: A message indicating why the query failed.
      List[Rowtype]: The values that were returned by the SQL statement.
    """
    global connection
    cursor:MySQLCursor = connection.cursor()
    cursor.execute(query)
    return Response(ResponseCode.OK), cursor.fetchall()
  # End of selectQuery()

  @staticmethod
  def dmlQuery(query:str) -> Response:
    """Sends a DML query to the MySQL Database.
    Args:
      query (str): The query to send to the database.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    global connection
    cursor:MySQLCursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return Response(Response.OK, f"Modified {DATABASE} Successfully.")
  # End of dmlQuery()

  @staticmethod
  def load_password() -> Response:
    """Retrieves the password to access the datbase from the associated .env file.
    Returns:
      Response: Whether or not the operation was successful, and a message that can be returned to the user.
    """
    if(load_dotenv()):
      global password
      password = getenv("DB_PASSWORD")
      return Response(ResponseCode.OK)
    return Response(ResponseCode.NOT_FOUND, """Environment file could not be found.""")
  # End of __load_password()
# End of Database