FROM python:3.8-slim

LABEL maintainer="<<USER>> <<<EMAIL>>>"

ENV PYTHONUNBUFFERED TRUE

WORKDIR /src/

COPY ./requirements.txt /src/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./<module-name>/ /src/<module-name>/
COPY ./test/ /src/test/

RUN py.test test/

WORKDIR /src/<module-name>/

ENTRYPOINT ["python", "<module-name>.py"]
CMD ["--help"]
