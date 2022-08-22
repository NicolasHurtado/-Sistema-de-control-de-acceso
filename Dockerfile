FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt
RUN ./migrations.sh 
CMD ["python", "manage.py", "runserver","0.0.0.0:8000"]