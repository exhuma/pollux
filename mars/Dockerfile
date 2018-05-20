FROM python:3
RUN apt-get update
RUN apt-get install -y \
    build-essential \
    libgrib2c-dev \
    libjasper-dev \
    libpng-dev \
    git

RUN pip install \
    numpy \
    pyproj

RUN git clone https://github.com/jswhit/pygrib
RUN apt-get install -y \
    libgrib-api-dev
RUN cd pygrib && python setup.py build
RUN cd pygrib && python setup.py install
