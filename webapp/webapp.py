from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context='adhoc', port=8080, debug=True)
