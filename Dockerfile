FROM python:3.9

COPY requirements.txt /project/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /project/requirements.txt

COPY app/ /project/app

WORKDIR /project/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]