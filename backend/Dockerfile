#Uses Python 3.10 as the base environment for the container
FROM python:3.10
#Creates a working folder named /app inside the container.
WORKDIR /app
#Copies all project files from your local backend folder into the Docker container.
COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000
#Starts the Flask application automatically when the container runs.
CMD ["python", "app.py"]