document.addEventListener("DOMContentLoaded", () => {
    const sendButton = document.getElementById("send_message");
    const userInput = document.getElementById("user_message");
    userInput.addEventListener('keyup', event => {
        event.preventDefault();
        if (event.key === "Enter") {
            sendButton.click();
        }
    })
})
