# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy script and requirements
COPY weather_report.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the script
#CMD ["python", "weather_report.py"]
# run in unbuffered mode for debug, so all statements flush directly to the logs.
CMD ["python", "-u", "weather_report.py"]