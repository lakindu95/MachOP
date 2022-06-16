FROM python:3.8

WORKDIR /code/

COPY ./ /code/

RUN python -m pip install -r requirements.txt \
    && rm -rf ~/.cache/pip   
     
EXPOSE 5100

ENV PYTHONPATH "${PYTHONPATH}:$PWD"