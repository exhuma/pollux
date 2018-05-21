Data Retrieval from ECMWF
=========================

See https://software.ecmwf.int/wiki/display/WEBAPI/Access+MARS


This folder contains two main utilities:

download.py
-----------

This downloads a year worth of data from the ECMWF CERA20C data set. The data
set is strongly limited to reduce download size and fetch time. It is limited
to a small number of variables and a small geographic region.

To run, use the provided ``Pipfile`` using ``pipenv``::

    # (if needed) pip install --user pipenv
    pipenv intstall
    pipenv run python download.py


extract.py
----------

This tool converts the variables from the CERA20C data-set to a 2D CSV file. It
assumes only one value per variable per day.

This is best run via the docker container buildable via the provided Dockerfile
due to required C libraries.

This is strongly dependent on the structure downloaded via ``download.py`` and
will likely need adaptation if ``download.py`` changes!

To run it::

    docker build -t exhuma/gribconvert .
    docker run \
        --rm \
        -v $(pwd)/data:/data exhuma/gribconvert \
        /data/2010.grib \
        /data/2010.csv
