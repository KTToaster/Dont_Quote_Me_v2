## IMPORTS ##
import mysql.connector
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from os import getenv
from dotenv import load_dotenv

from App.Helpers.Response import Response, ResponseCode

## GLOBALS ##
HOST = "127.0.0.1"  # Local for testing
USER = "root"
PORT = 3306 
DATABASE = "dqm_game"
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
    connection = mysql.connector.connect(user = USER,
      host = HOST,
      port=PORT,
      database = DATABASE,
      passwd = password)
    
  # End of connect()
  
  @staticmethod
  def disconnect() -> Response:
    global connection
    connection.disconnect()
  # End of disconnect()

  @staticmethod
  def send_query(query:str) -> Response:
    """Sends a query to the MySQL Database.
    Args:
      query (str): The query to send to the database.
    """
    global connection
    pass
  # End of query()

  ## PRIVATE METHODS ##
  def __load_password() -> Response:
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