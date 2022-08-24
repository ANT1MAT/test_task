FROM python:3.8
COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt
COPY . /code/
CMD [ "python", "/code/main.py"]
WORKDIR /code