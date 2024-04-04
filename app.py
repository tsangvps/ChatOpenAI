from flask import Flask, render_template, request
from flask_sse import sse
import Main
import datetime

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost:6379/0"  # URL của Redis để lưu trữ thông điệp SSE
app.register_blueprint(sse, url_prefix='/sse')  # Đăng ký blueprint SSE

time = datetime.datetime.now()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])

def send_message():
    global time
    data = request.get_json()
    if 'message' in data and 'phien' in data and 'id' in data:
        message = data['message']
        id = data['id']
        if(data['phien'] == "-1"):
            Main.user_token = Main.getToken
            Main.NewChat_ChatGPT(message, id)
        else:
            Main.Chat_ChatGPT(message, id, data['phien'])
        return "{'status': 'true'}"
    else:
        return "{'status': 'false', 'error': 'Invalid data format'}"

if __name__ == '__main__':
    app.run(debug=True)
