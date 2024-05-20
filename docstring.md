# Project DSA: dictionary documentation
## Class docstring
* There are some class which I implemented and used in this project
### Class definitions
| Class | Description | Destination |
| --- | --- | --- |
| `SQLDatabase` | Initialize a SQL database to store users' credentials | /app/database/initialize.py |
| `DataProcessor` | A class to process and prepare data for dictionary. Because the English - Vietnamese data is not clean and well - formatted so we need to turn it into a better one | /app/object/data.py |
| `Dictionary` | A dictionary implementation using trie data structure. It stores data in key - value format: English keyword as key, pronunciation and Vietnamese meaning as value | /app/object/dictionary.py |
| `UnicornException` | Class to catch HTTP error. I'm using Uvicorn engine to run the entire website but it doesn't have a standard class to catch HTTP Errors (like `Error 404`), so I made this class for that reason | /app/services/services.py |
|  |  |  |
### Class methods
<table>
  <tr>
    <th>Class</th>
    <th>Methods</th>
    <th>Description</th>
  </tr>


  <tr>
    <td rowspan="3"><code>SQLDatabase</code></td>
    <td><code>__init__(self)</code></td>
    <td>Automatically connect to back-end SQL database</td>
  </tr>
  <tr>
    <td><code>insert(hashed_username : str, hashed_password : str)</code></td>
    <td>Insert a new record to database.<br/>
    Parameters:</br>
    * hashed_username(str): user's hashed username</br>
    * hashed_password(str): user's hashed password
    </td>
  </tr>
  <tr>
    <td><code>query(username : str, password : str)</code></td>
    <td>Try to find the user. If the db returns 1 record, that means the credentials is valid.</br> 
    Parameters:</br>
        * username (str): user's login name</br>
        * password (str): user's password</br>      
    Return:</br>
        * Return length of result list. If length == 1, that mean the credential is correct
    </td>
  </tr>


  <tr>
    <td rowspan="2"><code>DataProcessor</code></td>
    <td><code>__init__(self, data_path : str)</code></td>
    <td>Initialize a processor for reading data from a file. Only support .txt file!</br>
    Parameters:</br>
        * data_path(str): the OS path to the destination which the dataset located
    </td>
  </tr>
  <tr>
    <td><code>process()</code></td>
    <td>Transform data from txt file to word - meaning pairs automatically.</br>
    Return:</br>
        * Return a list that contain well-formatted data
    </td>
  </tr>


  <tr>
    <td rowspan="4"><code>Dictionary</code></td>
    <td><code>__init__(self)</code></td>
    <td>Initialize dictionary's properties.</td>
  </tr>
  <tr>
    <td><code>create_node()</code></td>
    <td>Create a new dictionary node</br>
        Return:</br>
            * Return a trie node
    </td>
  </tr>
  <tr>
    <td><code>insert(word, meaning)</code></td>
    <td>Insert a new word and its meaning to dictionary. 
        If the word is inserted more than once, the last time will be used as the latest version.</br>
        Parameters:</br>
            * word (str): keyword to be inserted</br>
            * meaning (str): keyword's meaning</br>
        Return:</br>
            * None
    </td>
  </tr>
  <tr>
    <td><code>translate(word)</code></td>
    <td>Search for word and get the meaning.</br>
        Parameters:</br>
            * word (str): the keyword to be searched</br>
        Return:</br>
            * Return False if the word is not exists, otherwise return the word's meaning
    </td>
  </tr>    


  <tr>
    <td><code>UnicornException</code></td>
    <td><code>__init__(name: str)</code></td>
    <td>Initialize error name or code.</br>
    Parameters:</br>
    * name(str): error name or code
    </td>
  </tr>


</table>


## Fucntion docstring
* These docstring belong to some single functions that I initialized for my website. These function do not belong to any Python class.
### Function definitions
| Function | Description | Destination |
| --- | --- | --- |
| `encrypt(username : str, secret : str)` | Encrypt logged-in user data with strong secret key, using HMAC-SHA256 algorithm</br>Parameters:</br>* username (str): user's login name</br>* secret (str): hex-type secret key. Do not leak!</br>Return:</br>* Return a JWT token, use it for authentication purpose | /app/object/cookie.py |
| `decrypt(jwt_token : str, secret_key : str)` | Try to decrypt the user's login token. If the token is decrypted, that means the JWT token is valid.</br>Parameters:</br>* jwt_token (str): token string to decrypt</br>* secret_key (str): secret key to decrypt token</br>Return:</br>* Return True if the token is valid, else return False | /app/object/cookie.py |
| `ImportedDictionary()` | Automatically import English word to dictionary. It reads data from 'english-vietnamese.txt', processes (re-format) the data and returns the formatted data</br>Return:</br>* Return a data-filled dictionary | /app/object/importer.py |
| `suggestion(lst : list, word : str)` | If user enter some characters, suggest word based on the entered chars.</br>For example, if entered word is 'abs', the webapp will suggest all the keywords start with 'abs', like 'absolutely'</br>Parameters:</br>* lst (list): wordlist</br>* word (str): user's input keyword</br>Return:</br>* Return a list contains all the relevant keywords | /app/object/suggest.py |
| `is_logged_in(token : str)` | Check if user is logged in</br>Parameters:</br>* token (str): JWT token that user is holding</br>Return:</br>* Return True if the JWT login token is valid, else return False | /app/services/services.py |
| `validator(username : str, password : str)` | Check username and password rule.</br>Parameters:</br>* username (str): must be longer than 6 characters</br>* password (str): must have the length between 8 - 100 characters, must contain an uppercase, lowercase and number</br>Return:</br>* Return True if the conditions above are matched. Otherwise, return False | /app/services/services.py |
| `hasher(string : str)` | Hash the password before store to database</br>Parameters:</br>* string (str): string to be hashed</br>Return:</br>* Hashed string | /app/services/services.py |
| `login(request : Request)` | Login service interface for users</br>Parameters:</br>* request: user's request</br>Return:</br>* Return the login page to user | /app/services/services.py |
| `submit(request : Request)` | Submit login data to the server</br>Parameters:</br>* request: user's request</br>Return:</br>* Return the user's home page if login succeeded. Otherwise, return login page with a message | /app/services/services.py |
| `register(request : Request)` | Account registration user interface</br>Parameters:</br>* request: user's request</br>Return:</br>* Return registration page | /app/services/services.py |
| `submit(request : Request)` | Submit and save registration data to the server.</br>Parameters:</br>* request: user's request</br>Return:</br>* Return the login/registration page with a message | /app/services/services.py |
| `logout(request : Request)` | Log user out by deleting the JWT token</br>Parameters:</br>* request: user's request</br>Return:</br>* Return login page | /app/services/services.py |
| `query(request : Request, word : str \| None = None)` | Search for the entered word in the dictionary. If user didn't enter anything or the keyword is not exists, it will return an error message</br>Parameters:</br>* request: user's request</br>* word (str): keyword to be searched</br>Return:</br>* Return the keyword's meaning as a string. If the word has no meaning, return a message | /app/services/services.py |
| `home_page(request : Request, response : Response)` | Endpoint for the user's secret home page. Users will see a famous music video here :)</br>Parameters:</br>* request: user's request</br>* response: server's response</br>Return:</br>* Return user's home page when the user is logged in. Otherwise, redirect user to the login page with a message | /app/services/services.py |
| `root(request : Request)` | Main page of the website</br>Parameters:</br>* request: user's request</br>Return:</br>* index.html page | /app/services/services.py |
| `get_suggestion(request : Request, text : str)` | Endpoint for word suggestion service. Relevant keywords will be sent to user as suggestions</br>Parameters:</br>* request: user's request</br>* text (str): user's input text</br>Return:</br>* Return a list contains all the relevant keywords which will later be shown to user | /app/services/services.py |
| `error_404(request : Request, exception : UnicornException)` | Handle 404 error</br>Parameters:</br>* request: user's request</br>* exception: exception handler</br>Return:</br>Return error 404 page if the requested resource is not exists | /app/services/services.py |
|  |  |  |