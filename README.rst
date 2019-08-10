Pollen Alert Luxembourg
=======================

This package contains code for pollen information in Luxembourg via
http://www.pollen.lu

Fetching Data
-------------

Data on pollen.lu is only available via the HTML page. There is no API. This
Python package contains the console-script ``fetch_pollen_csv`` which downloads
a given date-range into a CSV file. Additionally, a subfolder ``cache`` will be
created to avoid unnecessary HTTP requests to the pollen.lu page. This
``cache`` folder will live in the current-working folder where
``fetch_pollen_csv`` is called.
