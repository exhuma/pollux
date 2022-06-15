Pollen Alert Luxembourg
=======================

This package contains code for pollen information in Luxembourg via
http://www.pollen.lu

It serves as a simple HTTP providing data-structures for a custom frontent
available at https://github.com/exhuma/pollux-frontend


Development Setup
-----------------

For convenience, a develpment environment can be initialised with fabric_ as
task-runner by running::

    fab develop

... and then running it using::

    fab run

If you don't have fabric, look into ``fabfile.py`` to see how the process is
set up.

.. _fabric: https://www.fabfile.org


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

    fab hashpw


Fetching Data
-------------

Data on http://www.pollen.lu is only available via the HTML page. There is no
API. This Python package contains the console-script ``fetch_pollen_csv`` (also
exposed via ``fab fetch-data``) which downloads a given date-range into a CSV
file. Additionally, a subfolder ``cache`` will be created to avoid unnecessary
HTTP requests to the pollen.lu page. This ``cache`` folder will live in the
current-working folder where ``fetch_pollen_csv`` is called.
