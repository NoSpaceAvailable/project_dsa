import sqlite3

class SQLDatabase:
    """Initialize a SQL database to store users' credentials"""
    def __init__(self) -> None:
        """Initialize a SQL database
        
        Return:
            * None
        """
        self.conn = sqlite3.connect("./app/database/accounts.db")       # Connect to database
        self.cursor = self.conn.cursor()                                # This is a cursor to control the database

        self.cursor.execute(
            # Create table if the table is not exists
            """CREATE TABLE IF NOT EXISTS users (
            username TEXT UNIQUE,
            password TEXT
            )"""
        )

        self.conn.commit()      # Commit the change of the database

    def insert(self, hashed_username : str, hashed_password : str) -> None:
        """Insert a new record to database
        
        Parameters:
            * hashed_username (str): hashed username string
            * hashed_password (str): hashed password string
            
        Return:
            * None
        """
        self.cursor.execute(
            "INSERT INTO users VALUES(?, ?)",
            (hashed_username, hashed_password)
        )

    def query(self, username : str, password : str) -> int:
        """Try to find the user. If the db returns 1 record, that means the credentials is valid
        
        Parameters:
            * username (str): user's login name
            * password (str): user's password
            
        Return:
            * Return length of result list. If length == 1, that mean the credential is correct
        """
        self.result = self.cursor.execute(
            "SELECT username, password FROM users WHERE username = ? and password = ?",
            (username, password)
        ).fetchall()
        return len(self.result)