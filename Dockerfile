FROM python:3.10-bullseye
ENV APP_DIR /app
WORKDIR ${APP_DIR}
COPY . ${APP_DIR}
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt
EXPOSE 5002
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "main:app"]
