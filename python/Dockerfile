# use TypedDict (see https://www.python.org/dev/peps/pep-0589/)
FROM python:3.8

LABEL author="Gus Hahn-Powell"
LABEL description="Image definition for basic Python 3.8 application"

# Create app directory
WORKDIR /app

# Bundle app source
COPY . .

RUN mv query.py /usr/local/bin/
RUN chmod u+x /usr/local/bin/*

# Install python dependencies
RUN pip install -U pip

RUN pip install -r requirements.txt

ENTRYPOINT ["query.py"]
#CMD ["query.py", "-h"]
