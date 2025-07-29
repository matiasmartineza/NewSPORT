import json
import os
import re
import unicodedata
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'change-me'

# Make the current username available in every template
@app.context_processor
def inject_username():
    return {'username': session.get('username')}

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
    return {}

def save_state():
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(STATE, f)

def get_user_state(username):
    user = STATE.setdefault(username, {d: {} for d in ["1", "2", "3", "4"]})
    return user

def clear_user_state(username):
    """Reset all stored progress for the given user."""
    STATE[username] = {d: {} for d in ["1", "2", "3", "4"]}
    save_state()

STATE = load_state()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = slugify(request.form.get('username', ''))
        if username:
            session['username'] = username
        return redirect(url_for('index'))

    username = session.get('username')
    if not username:
        return render_template('login.html')

    days = ["1", "2", "3", "4"]
    return render_template('index.html', days=days, username=username)

@app.route('/day/<day>', methods=['GET'])
def day_view(day):
    username = session.get('username')
    if not username:
        return redirect(url_for('index'))
    user_state = get_user_state(username)
    exercises = ROUTINES.get(day, [])
    done = user_state.get(day, {})
    return render_template('day.html', day=day, exercises=exercises, done=done)

@app.route('/logout')
def logout():
    """Clear user session and redirect to login."""
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/toggle/<day>/<int:idx>', methods=['POST'])
def toggle(day, idx):
    username = session.get('username')
    if not username:
        return ('', 400)
    user_state = get_user_state(username)
    state_day = user_state.setdefault(day, {})
    data = request.get_json(silent=True) or {}
    value = data.get('state')
    checked = False
    if isinstance(value, str):
        checked = value == 'checked'
    elif isinstance(value, bool):
        checked = value
    state_day[str(idx)] = checked
    save_state()
    return jsonify({str(idx): checked})

# New endpoint to reset all checkboxes for a day
@app.route('/reset/<day>', methods=['POST'])
def reset_day(day):
    """Clear the saved state for the given day."""
    username = session.get('username')
    if not username:
        return ('', 400)
    user_state = get_user_state(username)
    user_state[day] = {}
    save_state()
    return ('', 204)

@app.route('/exercise/<day>/<int:idx>', methods=['GET', 'POST'])
def exercise_view(day, idx):
    username = session.get('username')
    if not username:
        return redirect(url_for('index'))
    user_state = get_user_state(username)
    exercises = ROUTINES.get(day, [])
    if idx < 0 or idx >= len(exercises):
        return redirect(url_for('day_view', day=day))
    exercise = exercises[idx]
    if request.method == 'POST':
        state_day = user_state.setdefault(day, {})
        state_day[str(idx)] = True
        save_state()
        return redirect(url_for('day_view', day=day))
    done = user_state.get(day, {}).get(str(idx), False)
    return render_template('exercise.html', day=day, idx=idx, exercise=exercise, done=done)

@app.route('/summary/<day>', methods=['GET', 'POST'])
def summary(day):
    """Show summary of completed exercises for the given day."""
    username = session.get('username')
    if not username:
        return redirect(url_for('index'))
    # Reset user progress after finishing the routine
    clear_user_state(username)
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
                           percent=percent, muscles=muscles, counts=counts,
                           username=username)

if __name__ == '__main__':
    app.run(debug=True)
