from fastapi import FastAPI, Request, APIRouter, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database.initialize import SQLDatabase
from app.object.importer import ImportedDictionary
from app.object.cookie import encrypt, decrypt
from app.object.cookie import SECRET_KEY
from app.object.suggest import suggestion
from hashlib import sha1
import os
import re


class UnicornException(Exception):
    """Class to catch HTTP error"""
    def __init__(self, name: str):
        self.name = name


app = FastAPI()                                     # Initialize API
service = APIRouter()                               # Initialize webiste's endpoint routing service
template = Jinja2Templates(directory="templates")   # Define templates folder

suggest_list = open(                                # Open keyword file for word suggestion service
    "./app/object/keyword.txt", 
    encoding="UTF-8"
    ).readlines()


usr_regex = r'[a-zA-Z0-9_]{6,30}'                       # Username regex rule for account registration service
pw_regex = r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,100}'    # Password regex rule for account registration service


data = ImportedDictionary()     # A data - imported dictionary
db = SQLDatabase()              # Database to store user accounts


def is_logged_in(token : str) -> bool:
    """Check if user is logged in
    
    Parameters:
        * token (str): JWT token that user is holding
        
    Return:
        * Return True if the JWT login token is valid, else return False
    """
    return decrypt(
        # If user is using a valid key, the keey will be decrypted and the function will return True
        jwt_token = token,
        secret_key = SECRET_KEY
    )


def validator(username : str, password : str) -> bool:
    """Check username and password rule.
    
    Parameters:
        * username (str): must be longer than 6 characters 
        * password (str): must have the length between 8 - 100 characters, must contain an uppercase, lowercase and number

    Return:
        * Return True if the conditions above are matched. Otherwise, return False
    """
    if re.match(usr_regex, username) != None and re.match(pw_regex, password) != None:
        return True
    return False


def hasher(string : str) -> str:
    """Hash the password before store to database
    
    Parameters:
        * string (str): string to be hashed
        
    Return:
        * Hashed string
    """
    return sha1(bytes(string, encoding='UTF-8')).hexdigest()    # TODO: bug insert null value


@service.get("/login")
def login(request : Request):
    """Login service interface for users
    
    Parameters:
        * request: user's request
        
    Return:
        * Return the login page to user
    """
    token = request.cookies.get("session")
    if  is_logged_in(token):
        return RedirectResponse(
            url = "/home",
            status_code = 303,
        )
    msg = request.cookies.get("msg") if request.cookies.get("msg") else ""
    response = template.TemplateResponse(
        # Return html page
        "account.html",
        context = {
            "request" : request,
            "msg" : msg
        }
    )
    response.delete_cookie("session")   # Delete the logged-in token
    response.delete_cookie("username")
    response.delete_cookie("msg")
    return response


@service.post("/login")
async def submit(request : Request):
    """Submit login data to the server
    
    Parameters: 
        * request: user's request
        
    Return:
        * Return the user's home page if login succeeded. Otherwise, return login page with a message
    """
    form_data = await request.form()    # Get username and password from user
    _username = form_data.get("username")
    _password = hasher(form_data.get("password"))

    if db.query(_username, _password) == 1:
        """Check if the username and password is correct"""
        response = RedirectResponse(
            # If the username and password are correct, redirect user to homepage and set a logged-in token
            url = "/home",
            status_code = 303,
        )
        response.set_cookie("session", encrypt(form_data.get('username'), SECRET_KEY))
        response.set_cookie("username", _username)
        response.delete_cookie("msg")
        return response

    else:
        # If username and password are not correct, send a message
        return template.TemplateResponse(
            "account.html",
            context = {
                "request" : request,
                "msg" : "Account not found!"
            }
        )


@service.get("/register")
async def register(request : Request):
    """Account registration user interface
    
    Parameters:
        * request: user's request
        
    Return:
        * Return registration page
    """
    token = request.cookies.get("session")
    if  is_logged_in(token):
        return RedirectResponse(
            url = "/home",
            status_code = 303,
        )
    response = template.TemplateResponse(
        "account.html",
        context = {
            "request" : request
        }
    )
    response.delete_cookie("session")   # Delete the logged-in token
    response.delete_cookie("username")
    response.delete_cookie("msg")
    return response


@service.post("/register")
async def submit(request : Request):
    """Submit and save registration data to the server. 
    
    Parameters:
        * request: user's request
        
    Return:
        * Return the login/registration page with a message
    """
    form_data = await request.form()

    username = form_data.get("username")
    password = form_data.get("password")

    _username = username
    _password = hasher(password)

    if  db.query(_username, _password) and validator(username, password) == False:
        """Check if submitted credential is existed or not valid"""
        return template.TemplateResponse(
            # Return html page
            "account.html",
            context = {
                "request" : request,
                "msg" : "Registration failed. Username is not available or invalid username or password!"
            }
        )
    else:
        """Add account to the database"""
        db.insert(_username, _password)
        return template.TemplateResponse(
            # Return html page
            "account.html",
            context = {
                "request" : request,
                "msg" : "Registered successfully! Please sign in"
            }
        )
    

@service.get("/logout")
async def logout(request : Request):
    """Log user out by deleting the JWT token
    
    Parameters:
        * request: user's request
        
    Return:
        * Return login page
    """
    response = template.TemplateResponse(
        # Return html page
        "account.html",
        context = {
            "request" : request,
            "msg" : "Logged out!"
        }
    )
    response.delete_cookie("session")   # Delete the logged-in token
    response.delete_cookie("username")
    response.delete_cookie("msg")
    return response


@service.get("/query")
async def query(request : Request, word : str | None = None):
    """Search for the entered word in the dictionary. 
    If user didn't enter anything or the keyword is not exists, it will return an error message
    
    Parameters:
        * request: user's request
        * word (str): keyword to be searched
        
    Return:
        * Return the keyword's meaning as a string. If the word has no meaning, return a message
    """
    _word = ''
    result = ''
    if word:
        """If user enter a word, turn it to lowercase and search"""
        try:
            _word = word.lower().strip()
            result = data.translate(_word)
            if request.cookies.get("session") and request.cookies.get("username") and result:
                if is_logged_in(request.cookies.get("session")):
                    with open(f"./app/users/{hasher(request.cookies.get('username'))}.history.txt", "a") as history:
                        history.write(_word + "\n")
            if not result:
                result = "No result!"
        except:
            result = "No result!"
    else:
        result = "You haven't entered anything yet!"    # If user did not search anything
    return template.TemplateResponse(
        # Return the standard html page with word meaning
        "result.html",
        context = {
            "request" : request,
            "keyword" : _word,
            "meaning" : result
        }
    ) if result != "No result!" and result != "You haven't entered anything yet!" else template.TemplateResponse(
        "result.html",
        context = {
            # If there is no result or user didn't entered anything
            "request" : request,
            "error" : result
        }
    )


@service.get("/home")
async def home_page(request : Request, response : Response, history : str | None = None):
    """Endpoint for the user's secret home page. Users will see a famous music video here :)
    
    Parameters:
        * request: user's request
        * response: server's response
        
    Return:
        * Return user's home page when the user is logged in. Otherwise, redirect user to the login page with a message
    """
    token = request.cookies.get("session")
    username = request.cookies.get("username")
    if  is_logged_in(token):
        if history == "show":
            try:
                user_history = '\n'.join(open(f"./app/users/{hasher(request.cookies.get('username'))}.history.txt", "r").readlines()[-10:])
                return template.TemplateResponse(
                    # Return the standard home page
                    "home.html",
                    context = {
                        "request" : request,
                        "username" : username,
                        "history" : user_history
                    }
                )
            except:
                return template.TemplateResponse(
                    # Return the standard home page
                    "home.html",
                    context = {
                        "request" : request,
                        "username" : username,
                        "history" : "Nothing to show!"
                    }
                )
        elif history == "clear":
            try:
                os.remove(f"./app/users/{hasher(request.cookies.get('username'))}.history.txt")
            except:
                pass

        return template.TemplateResponse(
            # Return the standard home page
            "home.html",
            context = {
                "request" : request,
                "username" : username
            }
        )
    else:
        """If user is not logged in, return to index page"""
        return RedirectResponse(
            url = "/login",
            status_code = 303,
            headers = {
                "Set-Cookie" : "msg=Please sign in to continue!"
            }
        )
    

@service.get("/")
def root(request : Request):
    """Main page of the website
    
    Parameters:
        * request: user's request
    
    Return:
        * index.html page
    """
    return template.TemplateResponse(
        # Return index.html
        "index.html", 
        context = {
            "request" : request
            }
        )


@service.get("/suggestion")
async def get_suggestion(request : Request, text : str):
    """Endpoint for word suggestion service. Relevant keywords will be sent to user as suggestions
    
    Parameters:
        * request: user's request
        * text (str): user's input text
        
    Return:
        * Return a list contains all the relevant keywords which will later be shown to user
    """
    text = text.strip().lower()[:20]
    if text != '':
        result = suggestion(suggest_list, text)
        return result
    return []


@app.exception_handler(404)
def error_404(request : Request, exception : UnicornException):
    """Handle 404 error
    
    Parameters:
        * request: user's request
        * exception: exception handler
        
    Return:
        Return error 404 page if the requested resource is not exists
    """
    return template.TemplateResponse(
        # Return standard 404 not found page
        "error.html",
        context = {
            "request" : request,
            "error" : "Page not found!"
        },
        status_code = 404
    )


app.include_router(service)     # Include routing service to the website API
