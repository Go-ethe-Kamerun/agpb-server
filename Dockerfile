# inherit python image
FROM python:3.6

# setup directories
RUN mkdir /application

# copy python dependencies and instlall
COPY requirements.txt .
RUN pip install -R requirements.txt

# copy the rest of the application
COPY . .

EXPOSE 8001
STOPSIGNAL SIGINT

ENTRYPOINT ["python"]
CMD ["flask app.py"]
