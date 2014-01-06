glowing-turbo
=============

Python &amp; Flask (Python module) Backend for WonderfulPlanet MC Servers (http://wonderfulplanet.net)

Python from here: http://www.python.org/getit/releases/2.7.5/

Flask from here: http://flask.pocoo.org/

Make sure you have a file called "settings.py" in your root folder, which holds this data:

    params = {
        'host': 'your.hostname.net', # Host or IP
        'port': 20059, # Default
        'username': 'admin',
        'password': 'yourpass',
        'salt': '' # Not required with the new JSONAPI
    }


Once Python (with flask module) is installed, and screen is installed, execute these commands...:

    git clone https://github.com/Liamraystanley/glowing-turbo.git && cd glowing-turbo
    python app.py
