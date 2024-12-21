# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Collect static files
#ADD structo-entrypoint.sh /structo-entrypoint.sh
#RUN chmod a+x /structo-entrypoint.sh
#ENTRYPOINT ["/structo-entrypoint.sh"]

# Expose the port on which the Django app will run (by default 8000)
EXPOSE 8000

#
## Run the Django app
CMD ["gunicorn", "PalitraBlog.wsgi:application", "--bind", "0.0.0.0:8000", "--log-level", "debug", "--reload"]
