from flask import render_template, session, redirect, url_for
from core import main_dir
from core.config import config

import json


def admin():
    user = session.get('user')

    if not user or user.get('id') not in config.web_admins:
        return redirect(url_for('index.index_route'))

    with open(main_dir + '/lines.json') as f:
        lines = json.load(f)

    with open(main_dir + '/operators.json') as f:
        operators = json.load(f)

    operator = None
    if user and 'id' in user:
        operator = next((op for op in operators if user['id'] in op['users']), None)

    return render_template(
        'admin.html',
        user=user,
        operator=operator,
        admin=True,
        lines=lines
    )
