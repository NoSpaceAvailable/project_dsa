from datetime import datetime
from Crypto.Util.number import getRandomNBitInteger
import jwt


# A strong secret key so that no one could guess it
SECRET_KEY = str(getRandomNBitInteger(128))


def encrypt(username : str, secret : str) -> str:
    """Encrypt logged-in user data with strong secret key, using HMAC-SHA256 algorithm
    
    Parameters:
        * username (str): user's login name
        * secret (str): hex-type secret key. Do not leak!
        
    Return:
        * Return a JWT token, use it for authentication purpose
    """
    expiry = int(datetime.now().timestamp()) + 3600     # Set the expiration time for the logged-in token to 1 hour
    token = jwt.encode(
        # Use JWT token to store user's data
        {
            "username" : username,
            "exp" : expiry},
        key = secret,
        algorithm = "HS256",    # Using HMAC SHA256 encryption algorithm for safe
    )
    return token


def decrypt(jwt_token : str, secret_key : str) -> bool:
    """Try to decrypt the user's login token. If the token is decrypted, that means the JWT token is valid.
    
    Parameters:
        * jwt_token (str): token string to decrypt
        * secret_key (str): secret key to decrypt token
        
    Return:
        * Return True if the token is valid, else return False
    """
    try:
        res = jwt.decode(
            jwt = jwt_token,
            key = secret_key,
            algorithms = ["HS256"]
        )
        if res:
            # This mean the JWT token is valid. User can login now
            return True
        else:
            return False
    except:
        return False