# Python image to use.
FROM python:3.10-slim

# allow statements and log messages to appear
ENV PYTHONUNBUFFERED True

# copy local code to container image
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# install requirements
RUN pip install --no-cache-dir -r requirements.txt

# expose
EXPOSE 8080

# run server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
