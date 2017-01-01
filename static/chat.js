document.addEventListener("DOMContentLoaded", chat)

function chat() {

    // Connect to the Socket.IO server.
    // The connection URL has the format: http[s]://<domain>:<port>[/<namespace>]
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    var log = document.getElementById('log');
    log.scrollTop = log.scrollHeight;
    
    // Event handler for server sent data.
    // The callback function is invoked whenever the server emits data
    // to the client. The data is then displayed under "Received"
    socket.on('chat', function(msg) {
        var item = document.createElement('li');
        item.innerHTML = '<strong>' + msg.name + '</strong>: ' + msg.message;
        log.appendChild(item);
        log.scrollTop = log.scrollHeight;
    });

    // Handlers for the different forms in the page.
    // These accept data from the user and send it to the server
    var form = document.getElementById('broadcast');
    // Get user name stored on this device
    if (localStorage.name) {
    form[0].value = localStorage.name
    };

    form.addEventListener('submit', function(event) {
        localStorage.name = form[0].value;
        var message = {name:form[0].value, message:form[2].value};
        socket.emit('chat', message);
        form[2].value = '';
        return false;
    });
};
