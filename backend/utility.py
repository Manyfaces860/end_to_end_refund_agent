from random import Random

def retry_thing(func, retries=3, delay=1):
    
    def wrapper(*args, **kwargs):
        import time
        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Attempt {attempt + 1} failed with error: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)
        raise Exception(f"All {retries} attempts failed.")
    
    return wrapper

def create_new_session():
    return str(Random().randint(100000, 999999))

import google.auth
import google.auth.transport.requests

def get_fresh_gcp_token() -> str:
    """
    Automatically reads your Application Default Credentials file 
    and returns a valid, non-expired access token.
    """
    # This automatically tracks down the file mounted via Docker
    credentials, project = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    
    # Send a internal request to refresh the token if it's dead
    auth_request = google.auth.transport.requests.Request()
    credentials.refresh(auth_request)
    
    return credentials.token


