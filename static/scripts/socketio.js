document.addEventListener("DOMContentLoaded", () => {
    let socket = io.connect(`http://${document.domain}:${location.port}`);
    let room = "lounge";
    const sendButton = document.getElementById("send_message");
    const userInput = document.getElementById("user_message");
    const messageDisplayPanel = document.getElementById("message-display");
    const rooms = document.querySelectorAll(".select-room")
    const leaveRoom = (room) => {
        socket.emit('leave', { 'username': username, 'room': room });
    }
    const joinRoom = (room) => {
        socket.emit('join', { 'username': username, 'room': room });
        messageDisplayPanel.innerHTML = "";
    }
    const printSysMsg = (msg) => {
        const p = document.createElement('p');
        p.innerHTML = msg;
        messageDisplayPanel.append(p);
    }

    joinRoom(room)

    socket.on('message', (data) => {
        console.log(data)
        const p = document.createElement('p');
        if (data.username && data.time_stamp) {
            const span_username = document.createElement('span');
            const span_timestamp = document.createElement('span');
            span_username.innerHTML = data.username;
            span_timestamp.innerHTML = data.time_stamp;
            p.innerHTML = `${span_timestamp.outerHTML}: ${span_username.outerHTML} : ${data.msg}`;
        }
        else {
            p.innerHTML = `${data.msg}`;
        }
        messageDisplayPanel.append(p);
    });


    sendButton.onclick = () => {
        if (userInput.value != "") {
            socket.send({ 'msg': userInput.value, 'username': username, 'room': room });
            userInput.value = "";
        }
    };

    rooms.forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room) {
                msg = `You are already in ${room}.`
                printSysMsg(msg);
            }
            else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }
    })
})

