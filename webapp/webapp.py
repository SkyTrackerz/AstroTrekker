from flask import Flask, render_template, request, jsonify, Response
from flask_socketio import SocketIO

from Location import Location
from Programs.ManualControlProgram import ManualControlProgram
from Programs.StarTrackProgram import StarTrackProgram
from Programs.Utilities import ProgramUtilities
from StarTracker.StarTrackerService import StarTrackerService


class WebApp:
    def __init__(self, star_tracker_service: StarTrackerService):
        self.star_tracker_service = star_tracker_service

        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, logger=True)

        # Define Flask routes
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/submit_location', 'submit_location', self.submit_location, methods=['POST'])
        # Define Program routes
        self.app.add_url_rule('/programs', 'list_programs', self.list_programs)
        # Define SocketIO events
        self.socketio.on_event('joystick_update', self.handle_joystick_update)

    def index(self):
        return render_template('index.html')

    def submit_location(self):
        data = request.json
        if 'latitude' not in data or 'longitude' not in data or 'altitude' not in data:
            return jsonify({"failure": "Missing data"})
        latitude = data['latitude']
        longitude = data['longitude']
        altitude = data['altitude']

        print(f"Received location: Latitude = {latitude}, Longitude = {longitude}, Altitude = {altitude}")
        self.star_tracker_service.set_location(Location(latitude=latitude, longitude=longitude, elevation=altitude))

        # Process the data as needed
        return jsonify({"status": "success"})

    def list_programs(self):
        program_classes = ProgramUtilities.get_all_program_classes()  # Assumes this function is defined elsewhere
        program_names = [cls.__name__ for cls in program_classes]
        return jsonify(program_names)

    def program_schema(program_name):
        program_classes = ProgramUtilities.get_all_program_classes()  # Assumes this function is defined elsewhere
        for cls in program_classes:
            if cls.__name__ == program_name:
                if cls.Inputs is not None:
                    schema = ProgramUtilities.dataclass_to_json_schema(cls.Inputs)  # Assumes this function is defined elsewhere
                    return jsonify(schema)
                else:
                    return jsonify({"error": "No inputs defined for this program"}), 404
        return jsonify({"error": "Program not found"}), 404

    async def handle_joystick_update(self, message):
        if self.star_tracker_service.current_program is not ManualControlProgram:
            self.star_tracker_service.start_program(ManualControlProgram)
        print('Joystick X: {}, Y: {}'.format(message['x'], message['y']))
        await self.star_tracker_service.send_joystick_command(int(message['x']), int(message['y']))

        # Process joystick data here

    async def point_to_body(self):
        if self.star_tracker_service.location is None:
            return Response("Must set location to use star tracker", status=400)
        # Using jupiter initially
        print('Starting program TrackAstro')
        program = StarTrackProgram()
        self.star_tracker_service.start_program(program)

    def run(self):
        self.socketio.run(self.app, host='0.0.0.0', ssl_context='adhoc', port=8080, debug=True, allow_unsafe_werkzeug=True)


if __name__ == '__main__':
    my_app = WebApp()
    my_app.run()
