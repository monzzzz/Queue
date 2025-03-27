from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS
import os
import uuid

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")

EXCEL_FILE = "tasks.xlsx"


# Initialize Excel file if not exists
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["category", "number", "status"])
    df.to_excel(EXCEL_FILE, index=False)

scheduler = BackgroundScheduler()

def clear_excel_file():
    df = pd.DataFrame(columns=["category", "prefix", "number", "status"])
    df.to_excel(EXCEL_FILE, index=False)
    print(f"Excel file cleared at {datetime.now()}")

scheduler.add_job(clear_excel_file, 'cron', hour=0, minute=0, second=0, timezone='Asia/Bangkok')

# Start the scheduler
scheduler.start()

# Ensure the scheduler shuts down gracefully when the app is stopped


def load_tasks():
    try:
        return pd.read_excel(EXCEL_FILE)
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return pd.DataFrame(columns=["category", "number", "status"])

def save_tasks(df):
    df.to_excel(EXCEL_FILE, index=False)
    broadcast_tasks()

# ========================
# 🟢 Broadcast updated tasks to all clients
# ========================
def broadcast_tasks():
    df = load_tasks()
    # ✅ Fill NaN (None) values with an empty string to avoid serialization issues
    preparing = df[df['status'] == 'preparing'].fillna('').to_dict(orient='records')
    finished = df[df['status'] == 'finished'].fillna('').to_dict(orient='records')
    socketio.emit('update_tasks', {'preparing': preparing, 'finished': finished})
    

# ========================
# 🟢 Endpoint to Get Tasks
# ========================
@app.route('/tasks', methods=['GET'])
def get_tasks():
    df = load_tasks()
    preparing = df[df['status'] == 'preparing'].to_dict(orient='records')
    finished = df[df['status'] == 'finished'].to_dict(orient='records')
    return jsonify({'preparing': preparing, 'finished': finished})

# ========================
# 🟢 Endpoint to Add Task
# ========================
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    category = data.get('category')
    number = data.get('number')

    df = load_tasks()
    new_task = pd.DataFrame([{
        "task_id": str(uuid.uuid4()),
        "category": category,
        "number": number,
        "created_at": pd.Timestamp.now().isoformat(),
        "finished_at": None,
        "status": "preparing"
    }])
    df = pd.concat([df, new_task], ignore_index=True)
    save_tasks(df)

    return jsonify({'message': 'Task added successfully'}), 201

# ========================
# 🟢 Endpoint to Move Task to Finished
# ========================
@app.route('/tasks/finish', methods=['POST'])
def finish_task():
    data = request.json
    task_id = data.get('task_id')

    df = load_tasks()

    # ✅ Find task by "task_id" column instead of DataFrame index
    task_index = df.index[df['task_id'] == task_id].tolist()

    if task_index:
        task_index = task_index[0]  # Take the first match
        df.loc[task_index, 'status'] = 'finished'
        df.loc[task_index, 'finished_at'] = pd.Timestamp.now().isoformat()
        save_tasks(df)
        return jsonify({'message': 'Task marked as finished'}), 200

    return jsonify({'error': 'Invalid task'}), 400

# ========================
# 🟢 WebSocket Connection
# ========================
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    broadcast_tasks()

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# ========================
# 🟢 Start Flask Server with SocketIO
# ========================
if __name__ == '__main__':
    ssl_context = ('server.crt', 'server.key') 
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, ssl_context=ssl_context)