from flask import render_template, session, redirect, url_for
from core import main_dir
from core.config import config

import json


from flask import render_template, session, redirect, url_for
from core import main_dir
from core.config import config
import json

def operators():
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