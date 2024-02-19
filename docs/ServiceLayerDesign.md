### Star Tracker System Design with Manual Control via WebSocket
- Chatgpt convo: https://chat.openai.com/c/35b66771-65be-4439-8e62-5bfa0ed1cea4
- ```
  [Flask App] <--> [WebSocket/HTTP Routes]
      |
      V
  [Interaction Layer] (Translates requests to service commands)
      |
      V
  [StarTrackerService] (Central control logic)
      |                     |
      |---[IProgram]        |---[ManualControlCommand]
      |     ^   ^           |         |
      |     |   |-----------|         |
      |     |                         |
      |---[ManualControl]             
      |
      |     ^                          |
      |     |--------------------------|
      |
      |---[OtherPrograms] (e.g., AutoTrack, LookAtConstellation)
      |
      |---[MotorControl]
            |
            V
          [I3DMotor] <--> [3DMotor]
            |
            V
  		[IMotor] <--> [Motor]
  
  ```
	-
- #### Core Principles:
- Maintain separation of concerns.
- Use dependency injection for flexibility and testability.
- Ensure real-time interaction for manual control without cluttering the `StarTrackerService`.
- #### Components:
- -
- **Interfaces (Abstract Base Classes)**
- `IMotor`: Defines methods for zeroing and moving motors.
	- `I3DMotor`: Defines methods for pointing motors to a 3D point.
	- `IProgram`: Extended to support interaction capabilities with methods like `execute` and `handle_command`.
- -
- **Concrete Implementations**
- `ManualControl`: Implements `IProgram`, handling specific commands (e.g., joystick movements) via `handle_command`.
- -
- **Service Layer**
- `StarTrackerService`: Manages active programs and delegates user commands. Maintains the current program state and forwards commands to the active program.
- -
- **Flask Application with WebSocket Support**
- Handles real-time communication via WebSockets, translating user input into commands for the `StarTrackerService`.
- #### Detailed Design:
- -
- **Program Interface Extension**
- Programs support `handle_command(command_type, command_data)` for program-specific interactions.
- -
- **ManualControl Program**
- Processes joystick commands and other manual inputs, adjusting the tracker accordingly.
- -
- **StarTrackerService with State Management**
- Starts and manages programs.
	- Delegates incoming commands to the current active program.
- -
- **Flask App with WebSocket Integration**
- Uses Flask-SocketIO for WebSocket communication.
	- Routes `joystick_command` and other WebSocket events to the `StarTrackerService`.
- #### WebSocket Communication Flow:
- **Client to Flask App**: User sends a joystick movement via WebSocket.
- **Flask App to Service Layer**: Flask app receives the command and forwards it to `StarTrackerService`.
- **Service Layer to Program**: `StarTrackerService` delegates the command to the `ManualControl` program (if active).
- **Program Execution**: `ManualControl` processes the command, adjusting the tracker as needed.
- ### Implementation Notes:
- **Asynchronous Operation**: Ensure the manual control and program execution do not block the Flask app, allowing for continuous real-time interaction.
- **Program Flexibility**: Extend the `IProgram` interface to accommodate diverse interaction models for different tracking programs.
- **WebSocket for Real-Time Control**: Utilize WebSockets for a responsive control interface, essential for manual operation modes.
- This design encapsulates the complexity of real-time control and program management within the `StarTrackerService`, allowing the Flask app to remain a lightweight interface layer for user interaction.