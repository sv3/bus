
document.addEventListener("DOMContentLoaded", main)

function main() {

    // Connect to the Socket.IO server.
    // The connection URL has the format: http[s]://<domain>:<port>[/<namespace>]
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    
    // Event handler for server sent data.
    // The callback function is invoked whenever the server emits data
    // to the client. The data is then displayed under "Received"
    socket.on('message', function(msg) {
        // console.log(msg);
        msg = msg.toFixed(2)
        var rpmtext = document.getElementById("rpm");
        rpmtext.innerHTML = msg;
    });

};
