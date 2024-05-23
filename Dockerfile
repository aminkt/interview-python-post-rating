# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.10

# Set the working directory to /code
WORKDIR /app

# Install cron on linux
RUN apt update && apt install cron nano -y
# Copy the requirements file into the container at /code/
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE project.settings

# setup cronjob. it is good idea to move it in a shell script and add it later to prevent change
# dockerfile for adding new crons.
RUN { crontab -l; echo "0 */6 * * * /app/manage.py apply_queued_rates"; } | crontab -

# Run migrations and start the server
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
