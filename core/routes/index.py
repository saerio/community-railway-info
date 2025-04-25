from flask import render_template, session
from core import main_dir

import json


def index():
    user = session.get('user')
    
    with open(main_dir + '/lines.json') as f:
        lines = json.load(f)
    
    suspended_lines = []
    running_lines = []
    
    for line in lines:
        line_info = {
            'name': line['name'],
            'status': line['status'],
            'color': line.get('color', '#000000'),  # Default to black if no color specified
            'notice': line.get('notice', ''),
            'stations': line.get('stations', [])
        }
        
        if line['status'] == 'Suspended':
            suspended_lines.append(line_info)
        elif line['status'] == 'Running':
            running_lines.append(line_info)
        else:
            print(f"{line['name']} has an invalid status")
    
    return render_template(
        'index.html',
        user=user,
        suspended_lines=suspended_lines,
        running_lines=running_lines,
        lines=lines
    )
