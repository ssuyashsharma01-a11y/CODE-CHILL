# 🚀 PROJECT NEXUS: The Campus Nervous System
> **AI Fusion Hackathon 2026 Submission** | *Where Intelligence Meets Integration*

![Project Nexus Banner](https://via.placeholder.com/1000x300/0f172a/60a5fa?text=PROJECT+NEXUS+:+The+Ultimate+Campus+Super-App)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey?style=for-the-badge&logo=flask)
![AI/ML](https://img.shields.io/badge/AI-TextBlob%20%7C%20RapidFuzz-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Prototype%20Ready-success?style=for-the-badge)

## 📖 Overview
**Project Nexus** is not just an app; it is a **Unified Digital Ecosystem** designed to defragment the chaos of campus life into a single, seamless cockpit.

Most campus apps isolate features. Nexus **integrates** them. We leverage **AI/ML** to anticipate student needs—from summarizing long admin emails to finding lost items instantly using fuzzy logic matching.

---

## 🏆 Why This Project Wins
| Feature | Traditional App | 🚀 Project Nexus |
| :--- | :--- | :--- |
| **Communication** | Static Email Inbox | **AI Mail Summarizer & Deadline Extractor** |
| **Logistics** | Manual "Lost" Posters | **AI Fuzzy Matching for Lost Items** |
| **Academics** | PDF Timetables | **Live Context-Aware Dashboard** |
| **Navigation** | Asking Seniors | **AI Chatbot (NexusBot) & Explorer Maps** |

---

## 🌟 Key Features (The 4 Pillars)

### 1. 🎓 The Academic Cockpit
* **Live Schedule:** Automatically fetches classes based on the current day.
* **Smart Alerts:** "Next class is Data Structures in Room 202 starting in 10 mins."
* **Zero-Clutter UI:** Hides empty slots and holidays automatically.

### 2. 🥗 Daily Pulse (Smart Mess Menu)
* **Real-Time Menu:** Shows Breakfast, Lunch, or Dinner based on the hour.
* **Dietary Intelligence:** Clearly tags items as **Veg** or **Non-Veg**.
* **Crowd Meter:** Predicts mess rush hours (High/Medium/Low).

### 3. 🤖 Mail Intelligence (AI Powered)
* **NLP Summarization:** Compresses 500-word emails into 2-line action items.
* **Auto-Tagging:** Classifies emails as `Academic`, `Event`, or `Urgent`.
* **Deadline Detector:** Extracts dates ("Tomorrow", "5 PM") and highlights them in Red.

### 4. 🤝 Student Exchange (AI Lost & Found)
* **Fuzzy Matching Engine:** Uses Levenshtein Distance to match typos (e.g., "Blu Sony Headset" matches "Blue Sony Headphones").
* **Instant Alerts:** Users get a "Match Found" notification immediately upon reporting.

### 5. 💬 NexusBot (Campus Assistant)
* An integrated **Chatbot** that answers natural language queries:
    * *"What's for lunch?"*
    * *"Do I have class right now?"*
    * *"I lost my umbrella."*

---

## 🛠️ Tech Stack
* **Frontend:** HTML5, JavaScript (ES6), Tailwind CSS (Glassmorphism UI)
* **Backend:** Python (Flask)
* **AI/ML Engine:**
    * `TextBlob`: Natural Language Processing for summaries & sentiment.
    * `RapidFuzz`: String matching algorithms for Lost & Found.
    * `Regex`: Pattern recognition for timetable parsing.
* **Security:** Session-based Authentication with UID/Password.

---

## 📸 Screenshots
| **Secure Login** | **Unified Dashboard** |
|:---:|:---:|
| ![Login](https://via.placeholder.com/400x200/0f172a/ffffff?text=Secure+Login) | ![Dashboard](https://via.placeholder.com/400x200/0f172a/ffffff?text=Main+Dashboard) |

| **AI Mail Intelligence** | **NexusBot & Notifications** |
|:---:|:---:|
| ![Mail](https://via.placeholder.com/400x200/0f172a/ffffff?text=AI+Mail+Intel) | ![Chatbot](https://via.placeholder.com/400x200/0f172a/ffffff?text=Chatbot+Interface) |

---

## ⚡ How to Run Locally

### Prerequisites
* Python 3.x installed
* Git

### Installation Steps
1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/yourusername/project-nexus.git](https://github.com/yourusername/project-nexus.git)
    cd project-nexus
    ```

2.  **Install Dependencies**
    ```bash
    pip install flask textblob rapidfuzz
    ```

3.  **Run the Server**
    ```bash
    python app.py
    ```

4.  **Access the App**
    Open your browser and go to: `http://127.0.0.1:5000`

5.  **Login Credentials (Demo)**
    * **UID:** `25BAI70757`
    * **Password:** `12345678`

---

## 🧠 AI Implementation Details

#### 📧 Mail Summarizer Logic
We utilize a keyword-density algorithm combined with sentiment analysis to identify "Actionable Sentences."
```python
# Logic Snippet
keywords = ["urgent", "deadline", "tomorrow", "exam"]
if any(word in sentence for word in keywords):
    addToSummary(sentence)Lost & Found Matching
We use RapidFuzz to calculate a similarity ratio between the lost item description and found database entries.

Threshold: > 45% similarity triggers a match.

Benefit: Matches "Blue Bottle" with "Navy Water Flask" effectively.

🔮 Future Roadmap
[ ] AR Navigation: Augmented Reality pathfinding for campus blocks.

[ ] Uber-Pool for Campus: Cab sharing integration for students going to Chandigarh.

[ ] Voice Interface: Full voice command support for NexusBot.

👨‍💻 The Team
Built with ❤️ for AI Fusion Hackathon at IIT Ropar.

Suyash Sharma - Lead Developer & AI Architect

Navjot - Frontend Engineer & UI/UX

Eshaan - Backend Developer & Database Manager
