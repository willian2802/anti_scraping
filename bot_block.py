from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    user_ip = request.remote_addr
    return f"User IP: {user_ip}"

if __name__ == '__main__':
    app.run()

