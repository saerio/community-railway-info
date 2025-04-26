from flask import Blueprint, render_template, session, redirect, url_for
from core import main_dir
from core.config import config

import json
import requests

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
    
    avatar_base_url = "https://cdn.discordapp.com/avatars/"
    default_avatar = "https://cdn.discordapp.com/embed/avatars/0.png"

    if operator and 'users' in operator:
        operator['user_avatars'] = []
        for user_id in operator['users']:
            avatar_url = "https://avatar-cyan.vercel.app/api/" + user_id
            
            try:
                avatar_url = requests.get(avatar_url).json()
            except Exception:
                avatar_url = {"avatarUrl": default_avatar}
            
            operator['user_avatars'].append({
                'id': user_id,
                'avatar_url': avatar_url["avatarUrl"].replace("?size=512", "?size=32")
            })

    return render_template(
        'operator_lines.html',
        user=user,
        operator=operator,
        admin=admin,
        operator_lines=operator_lines
    )