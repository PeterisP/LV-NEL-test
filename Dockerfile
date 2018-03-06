FROM ubuntu:17.10

RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*

RUN pip3 install marisa-trie bottle requests

WORKDIR /opt/app
COPY *.py /opt/app/
COPY web /opt/app/
COPY wikidata/entities.json /opt/app/wikidata/

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED y

ENTRYPOINT ["/opt/app/nel_webservice.py"]
