from flask import Flask, jsonify
import socket, platform, uuid, psutil

from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/get_info')
def get_info():
    data = {
        'hostname': socket.gethostname(),
        'ipv4_address': socket.gethostbyname(socket.gethostname()),
        'mac_address': ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                                for ele in range(0, 8*6, 8)][::-1]),
        'os': platform.system(),
        'architecture': platform.machine(),
        'processor': platform.processor(),
        'cpu_cores': psutil.cpu_count(logical=False),
        'ram_total': f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
        'disk_usage': f"{round(psutil.disk_usage('/').used / (1024 ** 3), 2)} / {round(psutil.disk_usage('/').total / (1024 ** 3), 2)} GB",
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
