FROM python:3.8-slim

RUN apt-get update && apt-get install -y ffmpeg

COPY ./docker/requirements.txt /app/requirements.txt
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . /app

# Run the app
CMD ["python", "main.py"]


