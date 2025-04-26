from flask import Blueprint, session, redirect, url_for, render_template, request
from requests_oauthlib import OAuth2Session
from core.config import config
from core.url import *
from core import main_dir

import json


dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/dashboard')
async def dashboard_view():
    user = session.get('user')

    if not user:
        return redirect(url_for('auth.login'))

    with open(main_dir + '/lines.json') as f:
        lines = json.load(f)

    with open(main_dir + '/operators.json') as f:
        operators = json.load(f)

    operator = None
    admin = False

    if user and 'id' in user:
        operator = next(
            (op for op in operators if user['id'] in op['users']), None)

    if user and user["id"] in config.web_admins:
        admin = True

    if operator is None and not admin:
        return redirect(url_for('index'))

    operator_lines = []
    if operator:
        operator_lines = [
            line for line in lines
            if 'operator_uid' in line and line['operator_uid'] == operator['uid']
        ]

    return render_template(
        'dashboard.html',
        user=user,
        operator=operator,
        admin=admin,
        operator_lines=operator_lines
    )


@dashboard.route('/api/lines', methods=['POST'])
async def add_line():
    if not session.get('user'):
        return {'error': 'Unauthorized'}, 401

    try:
        data = request.json

        required_fields = ['name', 'color', 'status', 'operator_uid']
        for field in required_fields:
            if field not in data:
                print(f'Missing field: {field}')
                return {'error': f'Missing field: {field}'}, 400

        with open(main_dir + '/lines.json', 'r+') as f:
            lines = json.load(f)

            if any(line.get('name') == data['name'] for line in lines):
                return {'error': 'A line with that name already exists'}, 400

            lines.append(data)
            f.seek(0)
            json.dump(lines, f, indent=2)
            f.truncate()

        return {'success': True}, 200
    except Exception as e:
        return {'error': str(e)}, 500


@dashboard.route('/api/lines/<name>', methods=['PUT'])
async def update_line(name):
    if not session.get('user'):
        return {'error': 'Not authorized'}, 401

    try:
        data = request.json
        print(f"Updating line {name} with data:", data) 

        with open(main_dir + '/lines.json', 'r+') as f:
            lines = json.load(f)
            
            line_updated = False
            for i, line in enumerate(lines):
                if line.get('name') == name:
                    data['operator'] = line.get('operator')
                    data['operator_uid'] = line.get('operator_uid')
                    lines[i] = data
                    line_updated = True
                    break
            
            if not line_updated:
                return {'error': f'Line {name} not found'}, 404

            f.seek(0)
            json.dump(lines, f, indent=2)
            f.truncate()
            
        return {'success': True}, 200
    except Exception as e:
        print(f"Error while updating line {name}:", str(e))  
        return {'error': str(e)}, 500


@dashboard.route('/api/lines/<name>', methods=['DELETE'])
async def delete_line(name):
    if not session.get('user'):
        return {'error': 'Not authorized'}, 401

    try:
        with open(main_dir + '/lines.json', 'r+') as f:
            lines = json.load(f)
            lines = [line for line in lines if line.get('name') != name]
            f.seek(0)
            json.dump(lines, f, indent=2)
            f.truncate()

        return {'success': True}, 200
    except Exception as e:
        return {'error': str(e)}, 500
