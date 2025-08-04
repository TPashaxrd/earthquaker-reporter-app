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
                background: #121212;
                color: #eee;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
            }
            h1 {
                text-align: center;
                color: #ff4c4c;
                text-shadow: 0 0 8px #ff4c4c;
                margin-bottom: 30px;
            }
            ul {
                max-width: 600px;
                margin: 0 auto;
                padding: 0;
                list-style: none;
                border: 2px solid #ff4c4c;
                border-radius: 10px;
                background: #1f1f1f;
                box-shadow: 0 0 15px #ff4c4c;
            }
            li {
                padding: 15px 20px;
                border-bottom: 1px solid #333;
                font-size: 1.2em;
                letter-spacing: 0.05em;
            }
            li:last-child {
                border-bottom: none;
            }
            li:hover {
                background: #ff4c4c;
                color: #121212;
                cursor: default;
                transition: background 0.3s ease, color 0.3s ease;
            }
            @media (max-width: 640px) {
                body {
                    padding: 10px;
                }
                ul {
                    width: 100%;
                }
                li {
                    font-size: 1em;
                    padding: 10px 15px;
                }
            }
        </style>
    </head>
    <body>
        <h1>Latest Earthquakes</h1>
        <ul>
            {% for line in lines %}
                <li>{{ line|e }}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """, lines=lines)

def start_dashboard():
    threading.Thread(target=lambda: app.run(port=8080, debug=False, use_reloader=False), daemon=True).start()
