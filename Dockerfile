FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./__init__.py /code/__init__.py
COPY ./api /code/api
COPY ./draw /code/draw

CMD ["fastapi", "run", "api/main.py", "--port", "8001"]
