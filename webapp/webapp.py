from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, logger=True)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit_location', methods=['POST'])
def submit_location():
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']
    altitude = data['altitude']

    print(f"Received location: Latitude = {latitude}, Longitude = {longitude}, Altitude = {altitude}")

    # Process the data as needed
    return jsonify({"status": "success"})


@socketio.on('joystick_update')
def handle_joystick_update(message):
    print('Joystick X: {}, Y: {}'.format(message['x'], message['y']))
    # Process joystick data here (e.g., update game controls, send commands to a robot, etc.)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', ssl_context='adhoc', port=8080, debug=True)
