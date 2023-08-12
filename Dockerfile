FROM python:3.10-bullseye
WORKDIR /usr/src/app
COPY . /usr/src/app
EXPOSE 5002
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "main:app"]