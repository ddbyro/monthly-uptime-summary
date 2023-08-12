from flask import Flask, render_template, abort, url_for, jsonify
from prometheus_api_client import PrometheusConnect

import datetime
import json

app = Flask(__name__)
prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True)


def get_uptime():
    query = "sum(sum_over_time(probe_success{instance=~\".*\"}[30d])) / sum(count_over_time(probe_success{instance=~\".*\"}[30d])) * 100"

    return prom.custom_query(query)


def get_current_year():
    year = datetime.date.today().year

    return year


def get_current_month():
    mydate = datetime.datetime.now()

    return mydate.strftime("%B")


def create_json_package(year=None):
    monthly_uptime = {'monthly-uptime':
        [
            {
                'year': '',
                'month': '',
                'uptime': ''
            }
        ]
    }

    monthly_uptime.update(
        {'monthly-uptime':
            [
                {
                    'year': f'{year}',
                    'month': f'{get_current_month()}',
                    'uptime': f'{get_uptime()[0]["value"][1]}'
                }
            ]
        }
    )

    json_pkg = json.dumps(monthly_uptime, indent=4)

    return json_pkg


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


