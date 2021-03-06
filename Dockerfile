FROM mongo:xenial

RUN apt-get update
RUN apt-get install -y python3 python3-pip
WORKDIR /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt


# config file
RUN sed "/server_name/s/changeme.com/localhost/g" /app/core/config.py.sample > /app/core/config.py

RUN chmod +x /app/run.sh

# Make default port available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["./run.sh"]

