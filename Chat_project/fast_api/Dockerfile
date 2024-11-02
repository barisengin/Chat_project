FROM python:3.9

WORKDIR /app

COPY requirements.txt .

ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD . /app

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]