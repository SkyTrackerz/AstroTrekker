var socket = io();
//var joy = new JoyStick('joyDiv', {}, joystickCallback);
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(sendPositionToServer, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}
/*
function joystickCallback(joystickData) {
    console.log("x: " + joystickData.x + " y: " + joystickData.y);
    socket.emit('joystick_update', { x: joystickData.x, y: joystickData.y });
}*/

document.getElementById('cancel').addEventListener('click', function () {
    // Get the value from the editor

    fetch('/api/programs/cancel', {
        method: 'POST'
    })
});
function sendPositionToServer(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    const altitude = position.coords.altitude || 'Not available';

    fetch('/api/submit_location', {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ latitude, longitude, altitude }),
    })
        .then(response => response.json()) // parses JSON response into native JavaScript objects
        .then(data => {
            console.log(data);
            alert('Location sent to server!');
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Error sending location to server');
        });
}
function showError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            alert("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.");
            break;
    }
}
fetch('/api/programs')
    .then(response => response.json())
    .then(programs => {
        createEditor(programs);
    })
    .catch((error) => {
        console.error('Error:', error);
    });

function createEditor(programs) {
    var programSchemas = programs.map(programName => {
        return {
            $ref: `/api/programs/${programName}/schema`,
            title: programName
        };
    });
    JSONEditor.defaults.options.theme = 'bootstrap4';
    
        var editor = new JSONEditor(document.getElementById('editor_holder'), {
            ajax: true,
            schema: {
                type: "array",
                title: "Programs",
                //format: "tabs",
                items: {
                    title: "Program",
                    //headerTemplate: "{{i}} - {{self.name}}",
                    oneOf: programSchemas
                }
            },
            no_additional_properties: true,
            required_by_default: true,
            disable_edit_json: true,
            disable_properties: true,
            disable_collapse: true,
            use_name_attributes: true,
            disable_array_delete_last_row: true
        });
        
    /*
    JSONEditor.defaults.callbacks = {
        "button": {
            "myAction": function (jseditor, e) {
                alert('Button action')
            }
        }
    }
    */
    // Hook up the submit button to log to the console
    document.getElementById('submit').addEventListener('click', function () {
        // Get the value from the editor

        fetch('/api/programs', {
            method: 'POST', // or 'PUT'
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(editor.getValue()),
        })
        alert(JSON.stringify(editor.getValue()));

    });

    // Hook up the Restore to Default button

    /*
                // Hook up the validation indicator to update its 
                // status whenever the editor changes
                editor.on('change', function () {
                    // Get an array of errors from the validator
                    var errors = editor.validate();
    
                    var indicator = document.getElementById('valid_indicator');
    
                    // Not valid
                    if (errors.length) {
                        indicator.style.color = 'red';
                        indicator.textContent = "not valid";
                    }
                    // Valid
                    else {
                        indicator.style.color = 'green';
                        indicator.textContent = "valid";
                    }
                });
                */
}