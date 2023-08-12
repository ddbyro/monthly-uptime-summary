from flask import Flask, jsonify
from prometheus_api_client import PrometheusConnect
import yaml
import datetime
import json

# a = gunicorn(__name__)
app = Flask(__name__)
config = yaml.full_load(open('./config/config.yaml'))
prom = PrometheusConnect(url=f'{config["prod"]["hostname"]}:{config["prod"]["port"]}', disable_ssl=True)

def get_uptime():

    return prom.custom_query(config["prod"]["query"])


def get_current_year():
    year = datetime.date.today().year

    return year


def get_current_month():
    mydate = datetime.datetime.now()

    return mydate.strftime("%B")


@app.route("/json/")
def index():
    return jsonify(
        {
            'monthly-uptime': {
                f'{get_current_year()}': {
                    f'{get_current_month()}': f'{get_uptime()[0]["value"][1].strip()}'
                }
            }
        }
    )


if __name__ == '__main__':
    app.run(host='localhost', debug=True)


