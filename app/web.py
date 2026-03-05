from flask import Flask, render_template_string
from models.database import KickDB

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>KickArr Dashboard</title>
    <meta http-equiv="refresh" content="30">
    <style>
        body { font-family: sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; background: #f4f4f9; }
        h1 { color: #333; border-bottom: 2px solid #53e07d; padding-bottom: 0.5rem; }
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        th, td { text-align: left; padding: 1rem; border-bottom: 1px solid #eee; }
        th { background-color: #f8f9fa; font-weight: 600; color: #555; }
        tr:hover { background-color: #fcfcfc; }
        .status-completed { color: #28a745; font-weight: bold; }
        .status-failed { color: #dc3545; font-weight: bold; }
        .status-downloading { color: #fd7e14; font-weight: bold; animation: pulse 1.5s infinite; }
        .status-pending { color: #6c757d; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.6; } 100% { opacity: 1; } }
    </style>
</head>
<body>
    <h1>KickArr Dashboard</h1>
    <table>
        <thead>
            <tr>
                <th>Streamer</th>
                <th>Title</th>
                <th>Status</th>
                <th>Added At</th>
            </tr>
        </thead>
        <tbody>
            {% for vod in vods %}
            <tr>
                <td>{{ vod.streamer }}</td>
                <td>{{ vod.title }}</td>
                <td class="status-{{ vod.status }}">{{ vod.status|upper }}</td>
                <td>{{ vod.created_at }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    with KickDB() as db:
        vods = db.get_history()
    return render_template_string(TEMPLATE, vods=vods)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
