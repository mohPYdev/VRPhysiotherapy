// write a simple socket server in node and ws

const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 }, () => {
  console.log('Server started!');
});




wss.on('connection', function connection(ws) {
  ws.on('message', (data) => {
    console.log('received: %s', data);

    wss.clients.forEach(function each(client) {
      if (client.readyState === WebSocket.OPEN) {
        client.send(data.toString());
      }
    });

    // if (data == 'F') {
    //   ws.send('Error');
    // }  else if (data == "Start"){
    //   ws.send('Start');
    // }
    // else if (data == "End"){
    //   ws.send('End');
    // }
  });
});


wss.on('listening', () => {
    console.log('Server listening on port 8080!');
});

