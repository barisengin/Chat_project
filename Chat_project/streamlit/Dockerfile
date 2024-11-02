FROM python:3.9

WORKDIR /app

COPY requirements.txt .

ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD . /app

COPY . .

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py"]

# CMD ["sh", "-c", "python run_scripts.py; streamlit run app.py"]

# CMD ["streamlit", "run", "app.py","&&","python", "run_scripts.py"]