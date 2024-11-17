# Base image
FROM python:3.10-slim

RUN apt-get update && apt-get install -y nginx && apt-get clean

RUN pip install poetry==1.7.1

# Create working directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock /
COPY docker/app/start.sh /usr/local/bin/
RUN poetry install --without dev


# Expose application port
EXPOSE 8000

# Run the application
#CMD service nginx start && poetry run python /app/menu_planner/app.py
ENTRYPOINT ["start.sh"]
