FROM python:alpine3.6
ADD code /processor
WORKDIR /processor

# install dependencies
# the lapack package is only in the community repository
RUN echo "http://dl-4.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk --update add --no-cache \
    lapack-dev \
    gcc \
    freetype-dev

# Install dependencies
RUN apk add --no-cache --virtual .build-deps \
    gfortran \
    musl-dev \
    g++
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN pip install -r requirements.txt

# removing dependencies
RUN apk del .build-deps

CMD ["python", "run.py"]