FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=inverted_indices.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
