import json
import os
import re
import unicodedata
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def slugify(value: str) -> str:
    value = value.lower()
    value = unicodedata.normalize('NFKD', value)
    value = value.encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^a-z0-9]+', '-', value)
    return value.strip('-')

app.jinja_env.filters['slugify'] = slugify

STATE_FILE = 'state.txt'
ROUTINE_FILE = 'rutina.json'

# Load routine data
with open(ROUTINE_FILE, 'r', encoding='utf-8') as f:
    ROUTINES = json.load(f)

# Ensure days 1-4 exist
for d in ["1", "2", "3", "4"]:
    ROUTINES.setdefault(d, [])

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    # default empty state
    return {d: {} for d in ["1", "2", "3", "4"]}

def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f)

STATE = load_state()

@app.route('/')
def index():
    days = ["1", "2", "3", "4"]
    return render_template('index.html', days=days)

@app.route('/day/<day>', methods=['GET'])
def day_view(day):
    exercises = ROUTINES.get(day, [])
    done = STATE.get(day, {})
    return render_template('day.html', day=day, exercises=exercises, done=done)

@app.route('/toggle/<day>/<int:idx>', methods=['POST'])
def toggle(day, idx):
    state_day = STATE.setdefault(day, {})
    state_day[str(idx)] = not state_day.get(str(idx), False)
    save_state(STATE)
    return ('', 204)

# New endpoint to reset all checkboxes for a day
@app.route('/reset/<day>', methods=['POST'])
def reset_day(day):
    """Clear the saved state for the given day."""
    STATE[day] = {}
    save_state(STATE)
    return ('', 204)

@app.route('/exercise/<day>/<int:idx>', methods=['GET', 'POST'])
def exercise_view(day, idx):
    exercises = ROUTINES.get(day, [])
    if idx < 0 or idx >= len(exercises):
        return redirect(url_for('day_view', day=day))
    exercise = exercises[idx]
    if request.method == 'POST':
        state_day = STATE.setdefault(day, {})
        state_day[str(idx)] = True
        save_state(STATE)
        return redirect(url_for('day_view', day=day))
    done = STATE.get(day, {}).get(str(idx), False)
    return render_template('exercise.html', day=day, idx=idx, exercise=exercise, done=done)

@app.route('/summary/<day>', methods=['GET', 'POST'])
def summary(day):
    """Show summary of completed exercises for the given day."""
    exercises = ROUTINES.get(day, [])
    done_param = request.values.get('done', '')
    time_param = request.values.get('time', '0')
    try:
        total_time = int(time_param)
    except ValueError:
        total_time = 0

    done_idxs = []
    for part in done_param.split(','):
        if part.isdigit():
            done_idxs.append(int(part))

    percent = round(len(done_idxs) / len(exercises) * 100) if exercises else 0

    muscles = []
    counts = {}
    for i in done_idxs:
        if 0 <= i < len(exercises):
            target = exercises[i].get('target', 'Desconocido')
            muscles.append(target)
            counts[target] = counts.get(target, 0) + 1

    m = total_time // 60
    s = total_time % 60
    time_str = f"{m}:{s:02}"

    return render_template('summary.html', day=day, time=time_str,
                           percent=percent, muscles=muscles, counts=counts)

if __name__ == '__main__':
    app.run(debug=True)
