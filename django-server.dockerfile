FROM python:3.7


RUN mkdir -p /usr/src/ANNA/
ENV PYTHONPATH "/usr/src/ANNA"
WORKDIR /usr/src/

COPY . /usr/src/ANNA/
RUN pip install --no-cache-dir -r ANNA/requirements.txt
EXPOSE 8880

CMD ["python", "manage.py", "runserver"]