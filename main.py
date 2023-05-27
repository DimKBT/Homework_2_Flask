from flask import Flask

from flask import request

from faker import Faker

import csv

import requests

import json


app = Flask(__name__)


@app.route("/requirements/")
def requirements():
    '''
    requirements() view returns the list of dependencies,
    which used in current project
    '''
    with open("requirements.txt", "r") as f:
        return f.readlines()


@app.route('/generate-users/', methods=['GET', 'POST'])
def generate_users():
    '''
    generate-users() view gets from request an amount
    of fake users and returns the list of dictionaries, containing
    fake user name and email
    '''
    num_of_users = request.args.get('count', type=int)
    fake = Faker()
    list_to_return = [{fake.name(): fake.pystr(7, 7).lower()+'@mail.com'} for i in range(num_of_users)]
    return list_to_return


@app.route("/mean/")
def mean():
    '''
    mean() view returns average amounts of height and weight
    from the hw.csv
    '''
    with open("static/hw.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        total_height_inch = 0
        total_weight_pound = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            elif row == []:
                break
            else:
                total_height_inch = total_height_inch + float(row[1])
                total_weight_pound = total_weight_pound + float(row[2])
                line_count += 1
        height_average_cm = total_height_inch*2.54/(line_count-1)
        weight_average_kg = total_weight_pound*0.45359237/(line_count-1)
        return f'Average height is {height_average_cm:.0f} cm. Average weight is {weight_average_kg:.3f} kg'


@app.route("/space/")
def space():
    '''
    space() view returns the number of astronauts,
    have gotten from request
    '''
    r = requests.get('http://api.open-notify.org/astros.json')
    return f'{r.json()["number"]}'


if __name__ == '__main__':
    app.run(debug=True)


