import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

os.environ['API_KEY'] = 'f1fa4571a6fb452a91b2b60095bf34ee'

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def geocode(address):

    # Contact API
    try:

        url = "https://geoapify-platform.p.rapidapi.com/v1/geocode/search"

        api_key = os.environ.get("API_KEY")

        querystring = {"apiKey":f"{api_key}","text":f"{address}","lang":"en","limit":"1"}

        headers = {
            'x-rapidapi-key': "2f6fcd53f2msh15a7560e579605bp1d8128jsn093a0e5381ae",
            'x-rapidapi-host': "geoapify-platform.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        response.raise_for_status()

    except requests.RequestException:
        return None

    #parse response
    try:


        fresponse = response.json()


        return {
        "lon": fresponse['features'][0]['geometry']['coordinates'][0],
        "lat": fresponse['features'][0]['geometry']['coordinates'][1]
        }
    except (KeyError, TypeError, ValueError):
        return None




