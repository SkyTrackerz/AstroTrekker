from flask import Flask, render_template, request, jsonify, Response
from flask_socketio import SocketIO

from Location import Location
#from Programs.ManualControlService import ManualControlProgram
from Programs.StarTrackProgram import StarTrackProgram
from Programs.Utilities import ProgramUtilities
from StarTracker.MockStarTracker import MockStarTracker
from StarTracker.StarTrackerService import StarTrackerService


class WebApp:
    def __init__(self, star_tracker_service: StarTrackerService):
        self.star_tracker_service = star_tracker_service

        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, logger=True)

        # Define Flask routes
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/api/submit_location', 'submit_location', self.submit_location, methods=['POST'])
        # Define Program routes
        self.app.add_url_rule('/api/programs', 'list_programs', self.list_programs)
        self.app.add_url_rule('/api/programs', 'submit_programs', self.submit_programs, methods=['POST'])
        self.app.add_url_rule('/api/programs/<program_name>/schema', 'program_schema', self.program_schema, methods=['GET'])
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
        return jsonify({"status": "starting"})

    def list_programs(self):
        program_classes = ProgramUtilities.get_all_program_classes()
        program_names = [cls.__name__ for cls in program_classes]
        return jsonify(program_names)

    def program_schema(self, program_name: str):
        schema = ProgramUtilities.get_program_input_schema(program_name)
        if schema:
            return jsonify(schema)
        return jsonify({"error": "Program not found"}), 404
    
    def submit_programs(self):
        data = request.json
        # Check if data is None, not a list, or is an empty list
        if not data or not isinstance(data, list) or len(data) == 0:
            return jsonify({"error": "No programs submitted"}), 400
        try:
            programs = ProgramUtilities.create_programs_from_schema(data)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        return jsonify({"status": "success"})

    async def handle_joystick_update(self, message):
        pass
        #if self.star_tracker_service.current_program is not ManualControlProgram:
        #    self.star_tracker_service.start_program(ManualControlProgram)
        #print('Joystick X: {}, Y: {}'.format(message['x'], message['y']))
        #await self.star_tracker_service.send_joystick_command(int(message['x']), int(message['y']))

        # Process joystick data here

    async def point_to_body(self):
        if self.star_tracker_service.location is None:
            return Response("Must set location to use star tracker", status=400)
        # Using jupiter initially
        print('Starting program TrackAstro')
        program = StarTrackProgram()
        self.star_tracker_service.start_program(program)

    def run(self):
        self.socketio.run(self.app, host='0.0.0.0',
                          #ssl_context='adhoc',
                        port=8080, debug=True, allow_unsafe_werkzeug=True)


if __name__ == '__main__':
    mockStarTracker = MockStarTracker()
    starTrackerService = StarTrackerService(mockStarTracker)
    webapp = WebApp(starTrackerService)
    webapp.run()
