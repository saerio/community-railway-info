from flask import render_template, session
from core import main_dir

import json


def index():
    user = session.get('user')
    
    with open(main_dir + '/lines.json') as f:
        lines = json.load(f)
    
    suspended_lines = []
    running_lines = []
    possible_delays_lines = []
    no_scheduled_service = []
    
    for line in lines:
        line_info = {
            'name': line['name'],
            'status': line['status'],
            'color': line.get('color'), 
            'notice': line.get('notice', ''),
            'stations': line.get('stations', [])
        }
        
        match line["status"]:
            case "Suspended":
                suspended_lines.append(line_info)
            case "Running":
                running_lines.append(line_info)
            case "Possible delays":
                possible_delays_lines.append(line_info)
            case "No scheduled service":
                no_scheduled_service.append(line_info)
            case _:
                print(f"{line['name']} has an invalid status")
    
    return render_template(
        'index.html',
        user=user,
        suspended_lines=suspended_lines,
        running_lines=running_lines,
        possible_delays_lines=possible_delays_lines,
        no_scheduled_service=no_scheduled_service,
        lines=lines
    )
