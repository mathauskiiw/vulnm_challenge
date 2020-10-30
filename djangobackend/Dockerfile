# Use the official Python image from the Docker Hub
FROM python:3.8.5

# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Installs netcat
RUN apt-get update && apt-get install -y netcat

# Create app user in the app group
RUN useradd --user-group --create-home --no-log-init --shell /bin/bash app

ENV APP_HOME=/home/app/web

# Create staticfiles dir
RUN mkdir -p $APP_HOME/staticfiles

# Change the workdir
WORKDIR $APP_HOME

# Copy the requirements.txt file.
COPY ./requirements.txt $APP_HOME

# Upgrade pip
RUN pip install --upgrade pip

# Install the requirements.
RUN pip install -r requirements.txt

# Copy the rest of the code. 
COPY . $APP_HOME

RUN chown -R app:app $APP_HOME

USER app:app

ENTRYPOINT ["/home/app/web/entry.sh"]