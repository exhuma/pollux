Pollen Alert Luxembourg
=======================

This package contains code for pollen information in Luxembourg via
http://www.pollen.lu


Backend Configuration
---------------------

A sample config file can be found in ``pollux/default_settings.py``, copy it
and modify the settings as needed. Next, point the environment variable
``POLLUX_SETTINGS`` to that file. Example::

    cp pollux/default_settings.py mysettings.py
    POLLUX_SETTINGS="$(pwd)/mysettings.py" ... flask run


Authentication
--------------

By default usernames are taken from ``users.json`` in the current working
folder. The file has the following structure::

    {
      "john.doe@example.com": {
        "password": "<password-hash>",
        "permissions": [
          "upload_data"
        ]
      }
    }

To calculate a password hash, use::

    FLASK_APP="pollux.api:make_app()" ./env/bin/flask hashpassword


Fetching Data
-------------

Data on pollen.lu is only available via the HTML page. There is no API. This
Python package contains the console-script ``fetch_pollen_csv`` which downloads
a given date-range into a CSV file. Additionally, a subfolder ``cache`` will be
created to avoid unnecessary HTTP requests to the pollen.lu page. This
``cache`` folder will live in the current-working folder where
``fetch_pollen_csv`` is called.
