from prometheus_api_client import PrometheusConnect
from prometheus_client import start_http_server, Summary
import random
import time
import datetime
import json

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

if __name__ == '__main__':
    years = ("2022",'2023')
    for year in years:
        print(create_json_package(year=year))
