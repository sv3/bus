
document.addEventListener("DOMContentLoaded", main)

function main() {

    // Connect to the Socket.IO server.
    // The connection URL has the format: http[s]://<domain>:<port>[/<namespace>]
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Event handler for server sent data.
    // The callback function is invoked whenever the server emits data
    // to the client
    socket.on('rpm', function(msg) {
        var rpmtext = document.getElementById("rpm");
        rpmtext.innerHTML = msg.toFixed(2);
    });
    
    socket.on('atmo', function(msg) {
        var pressurespan = document.getElementById("pressure");
        var temperaturespan = document.getElementById("temperature");
        var humidityspan = document.getElementById("humidity");
        pressurespan.innerHTML = (msg.pressure / 1000).toFixed(2);
        temperaturespan.innerHTML = msg.temperature.toFixed(2);
        humidityspan.innerHTML = msg.humidity.toFixed(2);
    });

};
