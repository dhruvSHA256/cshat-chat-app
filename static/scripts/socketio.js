document.addEventListener("DOMContentLoaded", () => {
    // let socket = io.connect(`https://${document.domain}:${location.port}`);
    let socket = io.connect();

    let room = "lounge";
    const sendButton = document.getElementById("send_message");
    const userInput = document.getElementById("user_message");
    const messageDisplayPanel = document.getElementById("display-message-section");
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
        p.setAttribute("class", "system-msg");
        p.innerHTML = msg;
        messageDisplayPanel.append(p);
        scrollDownChatWindow()
        userInput.focus();
    }

    const scrollDownChatWindow = () => {
        const chatWindow = document.querySelector("#display-message-section");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    joinRoom(room)

    socket.on('message', (data) => {
        // console.log(data)
        const p = document.createElement('p');
        if (data.username && data.time_stamp) {
            const span_username = document.createElement('span');
            const span_timestamp = document.createElement('span');
            span_username.innerHTML = data.username;
            span_timestamp.innerHTML = data.time_stamp;
            if (data.username == username) {
                p.setAttribute("class", "my-msg");
                span_username.setAttribute("class", "my-username");
                span_timestamp.setAttribute("class", "timestamp");
                p.innerHTML = `${span_timestamp.outerHTML}: ${span_username.outerHTML} : ${data.msg}`;
                messageDisplayPanel.append(p);
            }

            else if (typeof data.username !== 'undefined') {
                p.setAttribute("class", "others-msg");
                span_username.setAttribute("class", "other-username");
                span_timestamp.setAttribute("class", "timestamp");
                p.innerHTML = `${span_timestamp.outerHTML}: ${span_username.outerHTML} : ${data.msg}`;
                messageDisplayPanel.append(p);
            }
        }
        else {
            printSysMsg(data.msg);
        }
        scrollDownChatWindow();
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
