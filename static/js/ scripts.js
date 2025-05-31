document.addEventListener("DOMContentLoaded", function () {
    console.log("StreamMe JS loaded! 🚀");

    // ✅ Back Button Functionality
    document.getElementById("backButton")?.addEventListener("click", function () {
        window.history.back();
    });

    // ✅ Video Playback Speed Control
    const videoPlayer = document.getElementById("videoPlayer");
    const videoSpeed = document.getElementById("videoSpeed");

    if (videoPlayer && videoSpeed) {
        videoSpeed.addEventListener("change", function () {
            videoPlayer.playbackRate = parseFloat(this.value);
            console.log(`Video speed set to ${this.value}x`);
        });
    }

    // ✅ Audio Playback Speed Control
    const audioPlayer = document.getElementById("audioPlayer");
    const playbackSpeed = document.getElementById("playbackSpeed");

    if (audioPlayer && playbackSpeed) {
        playbackSpeed.addEventListener("change", function () {
            audioPlayer.playbackRate = parseFloat(this.value);
            console.log(`Audio speed set to ${this.value}x`);
        });
    }

    // ✅ Audio Effects Handling (Reverb, Echo)
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

    // ✅ Search Functionality
    document.getElementById("searchForm")?.addEventListener("submit", function (event) {
        event.preventDefault();
        let query = document.getElementById("searchInput").value.trim();
        if (query) {
            window.location.href = `/search?query=${encodeURIComponent(query)}`;
        }
    });

    // ✅ Chatroom Messaging
    const socket = io();
    let nickname = "";

    document.getElementById("nicknameSet")?.addEventListener("click", function () {
        nickname = document.getElementById("nickname").value.trim();
        if (nickname) {
            socket.emit("join", nickname);
            document.getElementById("nickname").disabled = true;
        }
    });

    document.getElementById("sendMessage")?.addEventListener("click", function () {
        let message = document.getElementById("message").value.trim();
        if (message) {
            socket.emit("message", { nickname: nickname, text: message });
            document.getElementById("message").value = "";
        }
    });

    socket.on("message", function (data) {
        let chatBox = document.getElementById("chat-box");
        let msg = document.createElement("p");
        msg.innerHTML = `<strong>${data.nickname}:</strong> ${data.text}`;
        chatBox.appendChild(msg);
    });

    // ✅ Favorites Management
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

    // ✅ Comment Submission
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
