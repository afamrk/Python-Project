console.log('hai')
const sio = io();

sio.on('connect', () => {
    console.log('connected')
});

sio.on('disconnected', () => {
    console.log('disconnected')
});
