# inherit python image
FROM python:3.6

WORKDIR /app

# Create the directory for translations
RUN mkdir -p  agpb/db/data/trans/

COPY . /app

#grant permission to /app
RUN chmod -R 775 /app

# copy python dependencies and instlall
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy the rest of the application
COPY . .

STOPSIGNAL SIGINT

ENTRYPOINT [ "python" ]

CMD ["app.py"]
