document.addEventListener("DOMContentLoaded", function () {
    console.log("StreamMe JS loaded! 🚀");

    // ====== Back Button Functionality ======
    document.getElementById("backButton")?.addEventListener("click", function () {
        window.history.back();
    });

    // ====== Video Playback Speed Control ======
    const videoPlayer = document.getElementById("videoPlayer");
    const videoSpeed = document.getElementById("videoSpeed");

    if (videoPlayer && videoSpeed) {
        videoSpeed.addEventListener("change", function () {
            videoPlayer.playbackRate = parseFloat(this.value);
            console.log(`Video speed set to ${this.value}x`);
        });
    }

    // ====== Audio Playback Speed Control ======
    const audioPlayer = document.getElementById("audioPlayer");
    const playbackSpeed = document.getElementById("playbackSpeed");

    if (audioPlayer && playbackSpeed) {
        playbackSpeed.addEventListener("change", function () {
            audioPlayer.playbackRate = parseFloat(this.value);
            console.log(`Audio speed set to ${this.value}x`);
        });
    }

    // ====== Audio Effects Handling (Reverb, Echo) ======
    const soundEffect = document.getElementById("soundEffect");

    if (audioPlayer && soundEffect) {
        soundEffect.addEventListener("change", function () {
            if (this.value === "reverb") {
                audioPlayer.style.filter = "blur(2px)";
            } else if (this.value === "echo") {
                audioPlayer.style.filter = "brightness(1.2)";
            } else {
                audioPlayer.style.filter = "none";
            }
            console.log(`Sound effect set to ${this.value}`);
        });
    }

    // ====== Search Functionality ======
    document.getElementById("searchForm")?.addEventListener("submit", function (event) {
        event.preventDefault();
        let query = document.getElementById("searchInput").value.trim();
        if (query) {
            window.location.href = `/search?query=${encodeURIComponent(query)}`;
        }
    });

    // ====== Chatroom Messaging with Image & Voice Note Support ======
    const socket = io();
    let nickname = "";

    // Cache DOM elements for chatroom
    const nicknameInput = document.getElementById("nickname");
    const nicknameSetBtn = document.getElementById("nicknameSet");
    const messageInput = document.getElementById("message");
    const sendMessageBtn = document.getElementById("sendMessage");
    const chatBox = document.getElementById("chat-box");
    const imageUploadInput = document.getElementById("image-upload");
    const recordBtn = document.getElementById("record-btn");

    // Voice recording variables
    let mediaRecorder;
    let audioChunks = [];

    // Set nickname and join chat
    nicknameSetBtn?.addEventListener("click", function () {
        const nick = nicknameInput.value.trim();
        if (!nick) {
            alert("Please enter a nickname!");
            return;
        }
        nickname = nick;
        socket.emit("join", nickname);
        nicknameInput.disabled = true;
        nicknameSetBtn.disabled = true;
        messageInput.disabled = false;
        sendMessageBtn.disabled = false;
        if (imageUploadInput) imageUploadInput.disabled = false;
        if (recordBtn) recordBtn.disabled = false;
    });

    // Send text message
    sendMessageBtn?.addEventListener("click", function () {
        sendTextMessage();
    });

    // Also send message on Enter key in message input
    messageInput?.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            e.preventDefault();
            sendTextMessage();
        }
    });

    function sendTextMessage() {
        const text = messageInput.value.trim();
        if (!text) return;
        socket.emit("message", { nickname, text });
        messageInput.value = "";
    }

    // Receive text message
    socket.on("message", function (data) {
        addMessage(data.nickname, data.text);
    });

    // Receive image message
    socket.on("image", function (data) {
        addImage(data.nickname, data.image);
    });

    // Receive voice note
    socket.on("voice", function (data) {
        addVoiceNote(data.nickname, data.audio);
    });

    // Add message to chatbox (text)
    function addMessage(user, text) {
        const msg = document.createElement("p");
        msg.innerHTML = `<strong>${escapeHtml(user)}:</strong> ${escapeHtml(text)}`;
        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Add image message to chatbox
    function addImage(user, base64Image) {
        const msg = document.createElement("p");
        msg.innerHTML = `<strong>${escapeHtml(user)}:</strong><br><img src="${base64Image}" alt="image" style="max-width: 250px; max-height: 250px; border-radius: 8px;">`;
        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Add voice note to chatbox
    function addVoiceNote(user, base64Audio) {
        const msg = document.createElement("p");
        msg.innerHTML = `<strong>${escapeHtml(user)}:</strong><br><audio controls src="${base64Audio}"></audio>`;
        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Image upload handler
    imageUploadInput?.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function (e) {
            socket.emit("image", { nickname, image: e.target.result });
        };
        reader.readAsDataURL(file);

        // Reset input so same image can be uploaded again if needed
        event.target.value = "";
    });

    // Voice recording toggle
    recordBtn?.addEventListener("click", function () {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.stop();
            recordBtn.textContent = "Start Recording";
        } else {
            startRecording();
            recordBtn.textContent = "Stop Recording";
        }
    });

    function startRecording() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            alert("Your browser does not support audio recording.");
            return;
        }

        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.addEventListener("dataavailable", event => {
                    audioChunks.push(event.data);
                });

                mediaRecorder.addEventListener("stop", () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    const reader = new FileReader();
                    reader.onload = function (e) {
                        socket.emit("voice", { nickname, audio: e.target.result });
                    };
                    reader.readAsDataURL(audioBlob);
                });

                mediaRecorder.start();
            })
            .catch(err => {
                alert("Could not start audio recording: " + err);
            });
    }

    // Escape HTML to prevent XSS attacks
    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }

    // ====== Favorites Management ======
    document.querySelectorAll(".addFavorite").forEach(button => {
        button.addEventListener("click", function () {
            let songTitle = this.dataset.title;
            let songUrl = this.dataset.url;
            let userId = localStorage.getItem("userId") || "guest";

            fetch("/favorite", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: userId, song_title: songTitle, song_url: songUrl })
            }).then(response => response.json()).then(data => {
                console.log(data.message);
                alert(data.message);
            });
        });
    });

    // ====== Comment Submission ======
    document.querySelectorAll(".commentForm").forEach(form => {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            let songId = this.querySelector("input[name='song_id']").value;
            let text = this.querySelector("input[name='text']").value;
            let userId = localStorage.getItem("userId") || "guest";

            fetch("/comment", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: userId, song_id: songId, text: text })
            }).then(response => response.json()).then(data => {
                console.log(data.message);
                alert("Comment posted!");
                location.reload(); // Refresh to display new comments
            });
        });
    });
});
