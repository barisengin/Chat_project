FROM python:3.9

WORKDIR /app

COPY requirements.txt .

ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD . /app

COPY . .

# Consumer scriptini çalıştır
CMD ["python", "run_scripts.py"]