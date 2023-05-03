#FROM tiangolo/uwsgi-nginx-flask:python3.7
#FROM basin/py3-ml-flask:py3-ml-flask_0.1
FROM basin/py3-flask:py3-flask_0.1

#FROM alpine:3.2

ENV REFRESHED_AT 20151105

RUN apk --update add alpine-sdk xz poppler-dev pango-dev m4 libtool perl autoconf automake coreutils python-dev zlib-dev freetype-dev glib-dev cmake 
RUN cd / && \
git clone https://github.com/BWITS/fontforge.git && \
    cd fontforge && \
    ./bootstrap --force && \
    ./configure --without-iconv && \
    make && \
    make install && \
    cd / && \
    git clone git://github.com/coolwanglu/pdf2htmlEX.git && \
    cd pdf2htmlEX && \
    export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig && \
    cmake . && make && sudo make install && \
    apk del alpine-sdk xz poppler-dev pango-dev m4 libtool perl autoconf automake coreutils python-dev zlib-dev freetype-dev glib-dev cmake && \
    apk add libpng python freetype glib libintl libxml2 libltdl cairo poppler pango && \
    rm -rf /var/lib/apt/lists/* && \
    rm /var/cache/apk/* && \
    rm -rf /fontforge /libspiro /libuninameslist /pdf2htmlEX

VOLUME /pdf
WORKDIR /pdf


ENV STATIC_INDEX 1
#COPY ./app /app
RUN mkdir /app/logs
COPY ./pdftohtml /app/pdftohtml
COPY ./uwsgi.ini /app/uwsgi.ini
COPY ./requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
