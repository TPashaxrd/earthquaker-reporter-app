from flask import Flask, render_template_string
import threading

app = Flask(__name__)

@app.route('/')
def index():
    try:
        with open("earthquake_log.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()[-5:]
    except FileNotFoundError:
        lines = ["No records yet."]
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Latest Earthquakes</title>
    <style>
        body {
            min-height: 100vh;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #181c24 0%, #232946 100%);
            color: #eee;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .container {
            margin-top: 40px;
            background: #232946cc;
            border-radius: 18px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.25);
            padding: 32px 24px 24px 24px;
            max-width: 650px;
            width: 100%;
        }
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 18px;
        }
        .header-title {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .header-title h1 {
            font-size: 2.1em;
            color: #ff4c4c;
            margin: 0;
            text-shadow: 0 0 8px #ff4c4c55;
            letter-spacing: 0.03em;
        }
        .header-title .icon {
            font-size: 2em;
        }
        .subtitle {
            color: #b8b8b8;
            font-size: 1em;
            margin-top: 2px;
            margin-left: 4px;
        }
        .refresh-btn {
            background: #ff4c4c;
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 10px 18px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 2px 8px #ff4c4c33;
            transition: background 0.2s;
        }
        .refresh-btn:hover {
            background: #e63b3b;
        }
        ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        li {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 16px 18px;
            border-bottom: 1px solid #2d2d2d;
            font-size: 1.13em;
            background: rgba(255,255,255,0.01);
            transition: background 0.2s;
        }
        li:nth-child(even) {
            background: rgba(255,255,255,0.03);
        }
        li:last-child {
            border-bottom: none;
        }
        .quake-icon {
            font-size: 1.3em;
            color: #ff4c4c;
        }
        @media (max-width: 700px) {
            .container {
                padding: 16px 4px 12px 4px;
                margin-top: 10px;
            }
            .header-title h1 {
                font-size: 1.3em;
            }
            li {
                font-size: 1em;
                padding: 10px 6px;
            }
        }
    </style>
    <script>
        function refreshPage() {
            window.location.reload();
        }
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-title">
                <span class="icon">🌎</span>
                <div>
                    <h1>Latest Earthquakes</h1>
                    <div class="subtitle">Live updates from earthquake_log.txt</div>
                </div>
            </div>
            <button class="refresh-btn" onclick="refreshPage()">🔄 Refresh</button>
        </div>
        <ul>
            {% for line in lines %}
                <li><span class="quake-icon">⚡</span> {{ line|e }}</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
""", lines=lines)

def start_dashboard():
    threading.Thread(target=lambda: app.run(port=8080, debug=False, use_reloader=False), daemon=True).start()