from flask import Blueprint, render_template, session, redirect, url_for
from core import main_dir
from core.config import config

import json

operators = Blueprint('operators', __name__)

@operators.route('/operators')
def operators_route():
    user = session.get('user')

    with open(main_dir + '/lines.json') as f:
        lines = json.load(f)

    with open(main_dir + '/operators.json') as f:
        operators = json.load(f)

    for operator in operators:
        train_count = sum(1 for line in lines if line.get('operator_uid') == operator['uid'])
        operator['train_count'] = train_count

    operator = None
    if user and 'id' in user:
        operator = next((op for op in operators if user['id'] in op['users']), None)
    
    admin = False
    if user and user["id"] in config.web_admins:
        admin = True

    operators.sort(key=lambda x: x['name'])

    return render_template(
        'operators.html',
        user=user,
        admin=admin,
        operator=operator,
        operators=operators,
        lines=lines
    )
    
@operators.route('/operators/<string:uid>')
def operator_route(uid):
    user = session.get('user')

    with open(main_dir + '/lines.json') as f:
        lines = json.load(f)

    with open(main_dir + '/operators.json') as f:
        operators = json.load(f)

    operator = None
    admin = False

    operator = next((op for op in operators if op['uid'] == uid), None)

    if user and user["id"] in config.web_admins:
        admin = True

    operator_lines = []
    operator_lines = [
        line for line in lines
        if 'operator_uid' in line and line['operator_uid'] == uid
    ]

    return render_template(
        'operator_lines.html',
        user=user,
        operator=operator,
        admin=admin,
        operator_lines=operator_lines
    )