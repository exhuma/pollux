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
ADD extract.py /
RUN chmod +x /extract.py
RUN wget -O /tmp/wgrib.c ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib/wgrib.c
RUN (cd /tmp && gcc -o /usr/local/bin/wgrib wgrib.c)
ENTRYPOINT ["/extract.py"]
