// Open Sesame Node.js Version
//

var app = require('express')();
var httpServer = require('http').Server(app);
var io = require('socket.io')(httpServer);

// MESSAGE TYPES
// STARTUP_TYPE: Message Type that target device will send to open session
// REQUEST_TYPE: Message Type that triggers target device action
// ACK_TYPE: Message Type that target device sends back that confirms request fulfillment
// MISC_MSG_TYPE: Message Type for anything else
// DEBUG_TYPE: Message Type that was used for pinging between server and target device
// ERROR_MSG_TYPE: Message Type for error messages
var STARTUP_TYPE = "startup";
var REQUEST_TYPE = "request";
var ACK_TYPE = "ack";
var MISC_MSG_TYPE = "miscMsg";
var DEBUG_TYPE = "debug";
var ERROR_MSG_TYPE = "errorMsg";

var targetDeviceSocket = null;

var requestRoom = "requestRoom";

app.get('/', function(req,res) {
    res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket) {
    console.log('a user connected');

    socket.on('disconnect', function() {
        console.log('user disconnected');
        if(socket === targetDeviceSocket) {
            console.log('The target device has disconnected.');
            targetDeviceSocket = null;
        }
    });

    socket.on(STARTUP_TYPE, function(msg){
        console.log('The Target Device has connected');
        targetDeviceSocket = socket;
    });

    socket.on(MISC_MSG_TYPE, function(msg){
        console.log('message: ' + msg);
        io.emit(MISC_MSG_TYPE, msg);
    });

    socket.on(REQUEST_TYPE, function(msg){
        console.log('request received from client, forwarding request to target...');
        // send message only to the target device
        if(targetDeviceSocket !== null) {
            targetDeviceSocket.emit(REQUEST_TYPE,"");
            socket.join(requestRoom);
        } else {
            console.log('Target device is currently not connected');
            socket.emit(ERROR_MSG_TYPE,"Target device is currently not connected");
        }
        // TODO: Although currently to only one device, how to scale to more devices?
    });

    socket.on(ACK_TYPE, function(msg){
        console.log('request fulfillment received from target device. returning acknowledgement...');
        // TODO: What is best way to send back ack to requestor?
        io.to(requestRoom).emit(ACK_TYPE,"serverAck");
    });

});

httpServer.listen(3000, function() {
    console.log('listening on *:3000');
});



