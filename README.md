

### **README.md**
```markdown
# 🎵 Play API — Music & Video Streaming API

Play API allows users to **search**, **stream**, and **download** music or videos, powered by **Flask** and **yt-dlp**.  
It also provides **lyrics** for songs using an open-source API.

## ✨ Features
- 🔍 **Search for multiple songs** from YouTube
- 🎥 **Stream videos** directly on the website
- 🔊 **Play audio** without extra downloads
- 📜 **Get lyrics** for any song
- ⬇️ **Download songs/videos** with different quality options
- 🚀 **Built-in Docker support** for easy deployment

---

## 🚀 Installation

### 1️⃣ Clone this repository
```sh
git clone https://github.com/yourusername/play-api.git
cd play-api
```

### 2️⃣ Install dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Run Flask server
```sh
python app.py
```

### 4️⃣ Open in browser
Visit: `http://127.0.0.1:5000/`

---

## 📦 Docker Deployment
Want to run this API in a **Docker container**?
```sh
docker build -t play-api .
docker run -p 5000:5000 play-api
```

---

## 🌍 Render Deployment
Deploy this API on Render in **three simple steps:**
1. **Create a Render account** → [Render.com](https://render.com/)
2. **Create a new Web Service** → Select **GitHub Repo**
3. **Set Build & Start Commands**
   - Build: `pip install -r requirements.txt`
   - Start: `python app.py`

🚀 **Boom! Your API is live!**

---

## 🔥 API Endpoints
| Endpoint | Description |
|----------|------------|
| `/search?query=<song>` | Search for songs |
| `/play/audio?query=<song>` | Play audio |
| `/play/video?query=<song>` | Play video |
| `/lyrics?query=<song>` | Get song lyrics |
| `/download?video_url=<link>` | Download videos |

---

## ⚙️ Tech Stack
- **Flask** → Web framework
- **yt-dlp** → Video/audio downloading
- **Render** → Deployment platform
- **Docker** → Containerized setup
- **HTML & CSS** → Frontend UI

---

## 🛠 Contributing
Want to improve the Play API?  
Fork this repo and submit a **pull request!** 🚀  

---

## 📜 License
MIT License © 2025 heisbroken ✍️
