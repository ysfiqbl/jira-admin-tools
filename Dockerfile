FROM python:2.7-slim
MAINTAINER Yusuf Iqbal <yusuf.iqbal@devfactory.com>

# Set the application directory
WORKDIR /app

# Install our requirements.txt
ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy code from the current folder to /app inside the container
ADD . /app
