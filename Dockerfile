FROM ubuntu:latest
LABEL authors="farho"

ENTRYPOINT ["top", "-b"]