# Use an official Debian-based Python image as the base image
FROM python:3.11

# Set environment variables
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=lokeshrakurthi

# Install PostgreSQL
RUN apt-get update && \
    apt-get install -y postgresql postgresql-contrib && \
    apt-get clean

# Install additional packages
RUN apt-get update && \
    apt-get install -y \
        libpq-dev \
        build-essential \
        python3-dev \
    && apt-get clean

# Install Python packages using pip
RUN pip install psycopg2 pandas

# Create a directory for your project
WORKDIR /app

# Copy your project files into the container (you can replace this with your actual project files)
COPY . /app

# Expose the PostgreSQL port (default: 5432) if needed
EXPOSE 5432

# Start PostgreSQL service (optional, you can manually start it when needed)
CMD service postgresql start && [ "python", "testcode.py" ]
