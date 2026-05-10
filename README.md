# AI Chatbot with Real-Time APIs & DevOps

## 📌 Project Overview

This project is an AI-powered chatbot developed using Flask and React with integration of multiple real-time APIs. The chatbot provides dynamic responses for weather updates, cricket scores, news updates, and general AI-based conversations.

The main objective of this project is to demonstrate DevOps concepts such as CI/CD, containerization, version control, and cloud deployment using a real-world application.

---

## 🚀 Features

- 🌦 Real-time weather updates
- 🏏 Live cricket score updates
- 📰 Dynamic news retrieval
- 🤖 AI-based chatbot responses
- 🧠 Smart intent detection and routing

---

## 🧠 Smart Intent Detection

The chatbot uses a rule-based routing system:

- Weather queries → Weather API
- Cricket queries → Cricket API
- News queries → News API
- Other queries → OpenRouter AI

---

## 🛠 Technologies Used

### Frontend
- React.js
- HTML
- CSS

### Backend
- Flask
- Python

### APIs
- OpenWeather API
- CricAPI
- News API
- OpenRouter API

---

## ⚙️ DevOps Tools Used

| Tool | Purpose |
|---|---|
| Git & GitHub | Version control and code management |
| Docker | Containerization of Flask backend |
| Render | Cloud deployment and CI/CD |

---

## 🔄 CI/CD Workflow

1. Code changes made locally  
2. Changes pushed to GitHub  
3. Render detects GitHub updates automatically  
4. Application redeployed automatically  

---

## 🐳 Docker Usage

The Flask backend was containerized using Docker.

### Build Docker Image

```bash
docker build -t chatbot-backend .
```

### Run Docker Container

```bash
docker run -p 5000:5000 chatbot-backend
```

---

## 📂 Project Structure

```text
AI-CHATBOT-DEVOPS/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── backend/
│   ├── .env
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   ├── .gitignore
│   ├── package-lock.json
│   └── package.json
│
├── README.md
└── .gitignore
```

---

## ▶️ How to Run the Project

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm start
```

---

## 🌐 Deployment

The project is deployed using Render with GitHub auto-deployment.

Whenever code is pushed using:

```bash
git push
```

Render automatically redeploys the application.

---

## ✅ Improvements Implemented

- Dynamic weather city extraction
- Improved news query handling
- Better intent detection
- Reduced incorrect API routing
- Docker containerization
- CI/CD auto deployment

---

## 🎯 Conclusion

This project successfully demonstrates the integration of AI, real-time APIs, and DevOps practices.

The chatbot provides dynamic responses while implementing CI/CD automation, Docker containerization, and cloud deployment using modern DevOps tools.
