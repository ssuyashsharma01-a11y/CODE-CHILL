# =====================================================
# PROJECT NEXUS: FINAL LOGIN EDITION
# =====================================================

from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
from rapidfuzz import fuzz
import datetime
import re
import random
import os

app = Flask(__name__)
app.secret_key = "nexus_hackathon_secret_key"  # Required for Login Session

# =====================================================
# 1. DATABASE & CREDENTIALS
# =====================================================

USER_CREDENTIALS = {
    "uid": "25BAI70757",
    "password": "12345678"
}

MESS_MENU = {
    "Monday": {"Breakfast": "Aloo Paratha & Curd", "Lunch": "Rajma Chawal", "Dinner": "Mix Veg & Dal"},
    "Tuesday": {"Breakfast": "Puri Bhaji", "Lunch": "Kadi Pakoda", "Dinner": "Egg Curry / Paneer"},
    "Wednesday": {"Breakfast": "Idli Sambar", "Lunch": "Dal Makhani", "Dinner": "Chicken / Mushroom"},
    "Thursday": {"Breakfast": "Poha & Jalebi", "Lunch": "Chole Bhature", "Dinner": "Soyabean Curry"},
    "Friday": {"Breakfast": "Gobhi Paratha", "Lunch": "Rajma Chawal", "Dinner": "Fried Rice & Manchurian"},
    "Saturday": {"Breakfast": "Uttapam", "Lunch": "Khichdi & Achar", "Dinner": "Paneer Butter Masala"},
    "Sunday": {"Breakfast": "Chole Puri", "Lunch": "Biryani", "Dinner": "Dal Fry & Jeera Rice"}
}

TIMETABLE = {
    "Monday": [
        {"time": "09:00 - 10:00", "subject": "Mathematics (Linear Algebra)", "room": "LHC-101"},
        {"time": "10:00 - 11:00", "subject": "Data Structures & Algo", "room": "CS-202"},
        {"time": "14:00 - 16:00", "subject": "Physics Lab", "room": "PH-LAB"}
    ],
    "Tuesday": [
        {"time": "09:00 - 10:00", "subject": "Biology for Engineers", "room": "LHC-105"},
        {"time": "14:00 - 17:00", "subject": "Programming Practice Lab", "room": "CC-LAB-1"}
    ],
    "Wednesday": [
        {"time": "09:00 - 10:00", "subject": "Mathematics", "room": "LHC-101"},
        {"time": "11:00 - 12:00", "subject": "Intro to AI", "room": "CS-301"}
    ],
    "Thursday": [
        {"time": "10:00 - 11:00", "subject": "Soft Skills", "room": "LHC-205"},
        {"time": "14:00 - 16:00", "subject": "Engineering Drawing", "room": "ME-Drawing"}
    ],
    "Friday": [
        {"time": "09:00 - 10:00", "subject": "Mathematics", "room": "LHC-101"},
        {"time": "10:00 - 11:00", "subject": "Data Structures", "room": "CS-202"}
    ],
    "Saturday": [
        {"time": "10:00 - 12:00", "subject": "Club Activities", "room": "SAC"}
    ],
    "Sunday": []
}

ROPAR_SPOTS = [
    {"name": "Haveli Ropar", "vibe": "Chill & Food", "distance": "5 km"},
    {"name": "Satluj River Front", "vibe": "Nature & Peace", "distance": "2 km"},
    {"name": "IIT Ropar Library", "vibe": "Study & AC", "distance": "0.5 km"}
]

LOST_DB = [
    {"item": "Blue Sony Headphones", "location": "Library"},
    {"item": "Black Umbrella", "location": "Canteen"},
    {"item": "Calculator fx-991ES", "location": "LHC 101"}
]

# =====================================================
# 2. LOGIC ENGINES
# =====================================================

def ai_process_mail(text):
    text_lower = text.lower()
    raw_sentences = re.split(r'[.\n?!]', text)
    important_sentences = []
    keywords = ["urgent", "deadline", "tomorrow", "exam", "submit", "today", "attendance", "marks", "meeting", "room"]
    for sentence in raw_sentences:
        if any(word in sentence.lower() for word in keywords):
            clean_sent = sentence.strip()
            if len(clean_sent) > 5: important_sentences.append(clean_sent)
    summary = ". ".join(important_sentences) + "." if important_sentences else (raw_sentences[0] + ".")
    
    category = "General"
    if any(w in text_lower for w in ["exam", "quiz", "assignment"]): category = "Academic"
    elif any(w in text_lower for w in ["event", "hackathon", "club"]): category = "Event"
    
    priority = "Normal"
    if any(w in text_lower for w in ["urgent", "immediately", "deadline"]): priority = "High"

    deadline = "None"
    date_patterns = ["tomorrow", "today", "monday", "tuesday", "wednesday", "thursday", "friday"]
    for word in text_lower.split():
        clean_word = word.strip(",.!")
        if clean_word in date_patterns:
            deadline = clean_word.capitalize()
            break
            
    return {"summary": summary, "category": category, "priority": priority, "deadline": deadline}

def chatbot_response(msg):
    msg = msg.lower()
    day = datetime.datetime.now().strftime("%A")
    if any(w in msg for w in ["food", "mess", "lunch", "dinner", "breakfast", "menu"]):
        menu = MESS_MENU.get(day, MESS_MENU["Monday"])
        return f"Today is {day}. Lunch: {menu['Lunch']}. Dinner: {menu['Dinner']}."
    if any(w in msg for w in ["class", "lecture", "timetable"]):
        classes = TIMETABLE.get(day, [])
        if not classes: return "No classes today! 🎉"
        next_class = classes[0]
        return f"Next class: {next_class['subject']} at {next_class['time']} ({next_class['room']})."
    if any(w in msg for w in ["lost", "found"]): return "Check the 'Lost & Found' tab!"
    return "I can help with Mess Menu, Timetable, or Lost items."

def generate_notifications():
    notifs = []
    hour = datetime.datetime.now().hour
    if 8 <= hour <= 10: notifs.append({"type": "Mess", "msg": "Breakfast live: Aloo Paratha 🥞"})
    elif 12 <= hour <= 14: notifs.append({"type": "Mess", "msg": "Lunch serving: Rajma Chawal 🍛"})
    notifs.append({"type": "Academic", "msg": "Upcoming: Data Structures in CS-202 📚"})
    notifs.append({"type": "System", "msg": "NexusBot is online. Say Hi! 🤖"})
    return notifs

# =====================================================
# 3. API ROUTES
# =====================================================

@app.route("/")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template_string(DASHBOARD_HTML)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.json
        if data.get("uid") == USER_CREDENTIALS["uid"] and data.get("password") == USER_CREDENTIALS["password"]:
            session["logged_in"] = True
            return jsonify({"success": True})
        return jsonify({"success": False, "message": "Invalid Credentials"}), 401
    return render_template_string(LOGIN_HTML)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# --- DATA ROUTES ---
@app.route("/api/mess-data")
def mess_data(): return jsonify(MESS_MENU)

@app.route("/api/timetable-data")
def timetable_data(): return jsonify(TIMETABLE)

@app.route("/api/dashboard-data")
def dashboard_data():
    day = datetime.datetime.now().strftime("%A")
    return jsonify({"day": day, "spots": ROPAR_SPOTS})

@app.route("/api/notifications")
def notifications(): return jsonify(generate_notifications())

@app.route("/api/mail-summary", methods=["POST"])
def mail_summary():
    try:
        text = request.json.get("text", "")
        if not text: return jsonify({"error": "Empty text"}), 400
        return jsonify(ai_process_mail(text))
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route("/api/lost-found", methods=["POST"])
def lost_found():
    user_item = request.json.get("item", "")
    matches = []
    for entry in LOST_DB:
        score = fuzz.ratio(user_item.lower(), entry["item"].lower())
        if score > 45: matches.append(entry)
    return jsonify({"matches": matches})

@app.route("/api/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "")
    return jsonify({"response": chatbot_response(msg)})

# =====================================================
# 4. TEMPLATES (LOGIN & DASHBOARD)
# =====================================================

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login | Project Nexus</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #0f172a; color: white; font-family: 'Inter', sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .login-card { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); padding: 3rem; border-radius: 1.5rem; width: 100%; max-width: 400px; box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5); }
        .glow-text { text-shadow: 0 0 20px rgba(96, 165, 250, 0.5); }
        .input-field { background: #1e293b; border: 1px solid #334155; color: white; width: 100%; padding: 0.75rem; border-radius: 0.5rem; margin-bottom: 1rem; outline: none; transition: all 0.2s; }
        .input-field:focus { border-color: #60a5fa; box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2); }
        .btn-login { width: 100%; background: linear-gradient(to right, #3b82f6, #8b5cf6); padding: 0.75rem; border-radius: 0.5rem; font-weight: bold; transition: transform 0.1s; }
        .btn-login:hover { transform: translateY(-2px); }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="text-center mb-8">
            <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center font-bold text-3xl mx-auto mb-4 shadow-lg">N</div>
            <h1 class="text-2xl font-bold glow-text">PROJECT NEXUS</h1>
            <p class="text-gray-400 text-sm mt-1">Identify Yourself</p>
        </div>
        <div id="error-msg" class="hidden bg-red-500/10 border border-red-500 text-red-200 text-sm p-3 rounded mb-4 text-center"></div>
        <input type="text" id="uid" class="input-field" placeholder="User ID (e.g. 25BAI70757)">
        <input type="password" id="password" class="input-field" placeholder="Password">
        <button onclick="handleLogin()" id="login-btn" class="btn-login">INITIALIZE LINK</button>
    </div>

    <script>
        async function handleLogin() {
            const uid = document.getElementById('uid').value;
            const password = document.getElementById('password').value;
            const btn = document.getElementById('login-btn');
            const err = document.getElementById('error-msg');
            
            btn.innerText = "VERIFYING...";
            err.classList.add('hidden');
            
            try {
                const res = await fetch('/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({uid, password})
                });
                const data = await res.json();
                
                if (data.success) {
                    window.location.href = "/";
                } else {
                    err.innerText = "⚠️ Access Denied: Invalid ID or Password";
                    err.classList.remove('hidden');
                    btn.innerText = "INITIALIZE LINK";
                }
            } catch (e) {
                err.innerText = "Connection Error";
                err.classList.remove('hidden');
                btn.innerText = "INITIALIZE LINK";
            }
        }
        
        // Enter key support
        document.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') handleLogin();
        });
    </script>
</body>
</html>
"""

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard | Project Nexus</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/js/all.min.js"></script>
    <style>
        body { font-family: 'Inter', sans-serif; }
        .tab-btn { transition: all 0.3s ease; }
        .tab-btn.active { border-bottom: 3px solid #60a5fa; color: #60a5fa; background: rgba(30, 41, 59, 0.5); }
        .glass-panel { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }
        .animate-in { animation: fadeIn 0.5s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .badge { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 0.75rem; font-weight: bold; }
        #notif-dropdown { transform-origin: top right; transition: transform 0.2s ease-out, opacity 0.2s ease-out; }
        .notif-item { border-left: 3px solid #60a5fa; }
        #chat-window { transition: all 0.3s ease-in-out; }
        .chat-msg { max-width: 80%; padding: 8px 12px; border-radius: 12px; margin-bottom: 8px; font-size: 0.9rem; }
        .msg-user { background: #3b82f6; align-self: flex-end; color: white; border-bottom-right-radius: 2px; }
        .msg-bot { background: #374151; align-self: flex-start; color: #e5e7eb; border-bottom-left-radius: 2px; }
    </style>
</head>
<body class="bg-slate-900 text-white min-h-screen relative">

    <nav class="bg-slate-800 border-b border-slate-700 sticky top-0 z-50 shadow-lg">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex flex-col md:flex-row justify-between items-center md:h-16 py-2 md:py-0">
                <div class="flex items-center gap-2 mb-2 md:mb-0">
                    <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center font-bold shadow-lg">N</div>
                    <span class="text-xl font-bold tracking-tight">PROJECT NEXUS</span>
                </div>
                <div class="flex flex-wrap justify-center gap-1 md:gap-4 text-xs md:text-sm font-medium">
                    <button onclick="switchTab('academic')" id="btn-academic" class="tab-btn active px-3 py-2 md:py-5 rounded-t-lg">🎓 ACADEMIC</button>
                    <button onclick="switchTab('mess')" id="btn-mess" class="tab-btn px-3 py-2 md:py-5 rounded-t-lg hover:text-green-400">🥗 MESS</button>
                    <button onclick="switchTab('mail')" id="btn-mail" class="tab-btn px-3 py-2 md:py-5 rounded-t-lg hover:text-yellow-400">📧 MAIL</button>
                    <button onclick="switchTab('exchange')" id="btn-exchange" class="tab-btn px-3 py-2 md:py-5 rounded-t-lg hover:text-purple-400">🤝 L&F</button>
                    <button onclick="switchTab('explorer')" id="btn-explorer" class="tab-btn px-3 py-2 md:py-5 rounded-t-lg hover:text-orange-400">🧭 MAPS</button>
                </div>
                <div class="flex items-center gap-3 ml-4">
                    <div class="relative">
                        <button onclick="toggleNotifs()" class="relative p-2 text-gray-400 hover:text-white transition"><i class="fas fa-bell text-xl"></i><span class="absolute top-1 right-1 w-3 h-3 bg-red-500 rounded-full border-2 border-slate-800"></span></button>
                        <div id="notif-dropdown" class="absolute right-0 mt-2 w-80 bg-slate-800 border border-slate-700 rounded-xl shadow-2xl hidden z-50 overflow-hidden"><div class="p-3 border-b border-slate-700 font-bold text-sm bg-slate-900/50">Notifications</div><div id="notif-list" class="max-h-64 overflow-y-auto"></div></div>
                    </div>
                    <a href="/logout" class="bg-red-600/20 text-red-400 hover:bg-red-600/40 px-3 py-1 rounded text-xs font-bold border border-red-600/50">LOGOUT</a>
                </div>
            </div>
        </div>
    </nav>

    <main class="max-w-6xl mx-auto p-4 md:p-6 mt-4 pb-20">
        <section id="tab-academic" class="tab-content animate-in">
            <div class="glass-panel p-8 rounded-2xl border-l-4 border-blue-500">
                <div class="flex justify-between items-center mb-6"><div><h2 class="text-3xl font-bold text-blue-400">Academic Cockpit</h2><p class="text-gray-400 text-sm">Live Class Schedule</p></div><div class="flex items-center gap-2"><span class="text-sm text-gray-400">Day:</span><select id="timetable-day-select" onchange="updateTimetableDisplay()" class="bg-slate-800 border border-slate-600 rounded px-3 py-2 text-sm focus:border-blue-500 outline-none text-white"><option value="Monday">Monday</option><option value="Tuesday">Tuesday</option><option value="Wednesday">Wednesday</option><option value="Thursday">Thursday</option><option value="Friday">Friday</option><option value="Saturday">Saturday</option></select></div></div>
                <div id="timetable-list" class="space-y-4"></div>
                <div id="no-classes-msg" class="hidden text-center py-10 text-gray-500"><i class="fas fa-mug-hot text-4xl mb-2"></i><p>No classes scheduled for this day.</p></div>
            </div>
        </section>
        <section id="tab-mess" class="tab-content hidden animate-in">
            <div class="glass-panel p-8 rounded-2xl border-l-4 border-green-500">
                <div class="flex justify-between items-center mb-8"><div><h2 class="text-3xl font-bold text-green-400">Daily Pulse: Mess</h2><p class="text-gray-400">Real-time nutritional tracking</p></div><div class="flex items-center gap-2"><label class="text-sm text-gray-400">Day:</label><select id="mess-day-select" onchange="updateMessDisplay()" class="bg-slate-800 border border-slate-600 rounded px-3 py-2 text-sm focus:border-green-500 outline-none"><option value="Monday">Monday</option><option value="Tuesday">Tuesday</option><option value="Wednesday">Wednesday</option><option value="Thursday">Thursday</option><option value="Friday">Friday</option><option value="Saturday">Saturday</option><option value="Sunday">Sunday</option></select></div></div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="bg-slate-800/50 p-6 rounded-xl border border-slate-700 hover:border-green-500/50 transition"><div class="text-4xl mb-4">☕</div><p class="text-xs text-green-400 uppercase font-bold tracking-wider mb-1">Breakfast</p><p id="mess-bf" class="text-xl font-medium">Loading...</p></div>
                    <div class="bg-slate-800/50 p-6 rounded-xl border border-slate-700 hover:border-green-500/50 transition"><div class="text-4xl mb-4">🍛</div><p class="text-xs text-green-400 uppercase font-bold tracking-wider mb-1">Lunch</p><p id="mess-lunch" class="text-xl font-medium">Loading...</p></div>
                    <div class="bg-slate-800/50 p-6 rounded-xl border border-slate-700 hover:border-green-500/50 transition"><div class="text-4xl mb-4">🍲</div><p class="text-xs text-green-400 uppercase font-bold tracking-wider mb-1">Dinner</p><p id="mess-dinner" class="text-xl font-medium">Loading...</p></div>
                </div>
            </div>
        </section>
        <section id="tab-mail" class="tab-content hidden animate-in">
            <div class="glass-panel p-8 rounded-2xl border-l-4 border-yellow-500">
                <div class="mb-6"><h2 class="text-3xl font-bold text-yellow-400">Mail Intelligence 🤖</h2><p class="text-gray-400">AI-powered summarization & tagging.</p></div>
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div class="space-y-4">
                        <textarea id="mail-input" class="w-full h-64 bg-slate-800 p-4 rounded-xl border border-slate-700 focus:ring-2 focus:ring-yellow-500 outline-none text-gray-300 font-mono text-sm" placeholder="Paste the long email body here..."></textarea>
                        <button onclick="summarizeMail()" id="mail-btn" class="w-full bg-yellow-600 hover:bg-yellow-500 text-black font-bold py-3 rounded-xl transition shadow-lg shadow-yellow-900/20">⚡ Analyze & Summarize</button>
                    </div>
                    <div id="mail-result-container" class="bg-slate-800 rounded-xl p-6 border border-slate-700 relative hidden">
                        <div class="flex gap-2 mb-4" id="ai-tags"></div>
                        <div class="mb-4 pb-4 border-b border-slate-600"><p class="text-xs text-gray-500 uppercase font-bold">DEADLINE / DATE</p><p id="mail-deadline" class="text-xl text-white font-bold">--</p></div>
                        <h3 class="text-yellow-400 font-bold mb-2">Key Action Items</h3>
                        <p id="mail-summary-text" class="text-gray-200 leading-relaxed text-sm"></p>
                    </div>
                </div>
            </div>
        </section>
        <section id="tab-exchange" class="tab-content hidden animate-in">
            <div class="glass-panel p-8 rounded-2xl border-l-4 border-purple-500">
                <div class="text-center mb-8"><h2 class="text-3xl font-bold text-purple-400">Student Exchange</h2><p class="text-gray-400">AI-Powered Lost & Found Matching</p></div>
                <div class="max-w-xl mx-auto">
                    <div class="flex gap-2 mb-6">
                        <input id="lost-item" type="text" placeholder="Describe lost item (e.g. Blue Umbrella)" class="flex-1 bg-slate-800 border border-slate-600 p-4 rounded-xl text-lg focus:border-purple-500 outline-none">
                        <button onclick="findItem()" class="bg-purple-600 hover:bg-purple-500 px-8 rounded-xl font-bold text-lg shadow-lg shadow-purple-900/20">Scan</button>
                    </div>
                    <div id="lost-results" class="space-y-2"></div>
                </div>
            </div>
        </section>
        <section id="tab-explorer" class="tab-content hidden animate-in">
            <div class="glass-panel p-8 rounded-2xl border-l-4 border-orange-500">
                <div class="mb-6"><h2 class="text-3xl font-bold text-orange-400">Explorer's Guide</h2><p class="text-gray-400">Discover Ropar based on your vibe.</p></div>
                <div id="spots-list" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"></div>
            </div>
        </section>
    </main>

    <div id="chat-widget" class="fixed bottom-6 right-6 z-50 flex flex-col items-end">
        <div id="chat-window" class="hidden bg-slate-800 border border-slate-700 w-80 h-96 rounded-2xl shadow-2xl flex flex-col overflow-hidden mb-4">
            <div class="bg-blue-600 p-3 flex justify-between items-center"><div class="font-bold text-sm">🤖 NexusBot</div><button onclick="toggleChat()" class="text-white hover:text-gray-300"><i class="fas fa-times"></i></button></div>
            <div id="chat-history" class="flex-1 p-3 overflow-y-auto flex flex-col gap-2"><div class="chat-msg msg-bot">Hi! I'm NexusBot. Ask me about classes, food, or lost items!</div></div>
            <div class="p-2 bg-slate-900 flex gap-2"><input id="chat-input" class="flex-1 bg-slate-800 border border-slate-700 rounded-full px-4 py-2 text-sm focus:border-blue-500 outline-none" placeholder="Ask something..." onkeypress="handleChatKey(event)"><button onclick="sendChat()" class="bg-blue-600 hover:bg-blue-500 w-10 h-10 rounded-full flex items-center justify-center transition"><i class="fas fa-paper-plane text-xs"></i></button></div>
        </div>
        <button onclick="toggleChat()" class="bg-blue-600 hover:bg-blue-500 w-14 h-14 rounded-full shadow-2xl flex items-center justify-center transition transform hover:scale-110"><i class="fas fa-comment-dots text-2xl"></i></button>
    </div>

    <script>
        let globalMessMenu = {}; let globalTimetable = {};
        function switchTab(t) { document.querySelectorAll('.tab-content').forEach(e=>e.classList.add('hidden')); document.querySelectorAll('.tab-btn').forEach(e=>e.classList.remove('active')); document.getElementById('tab-'+t).classList.remove('hidden'); document.getElementById('btn-'+t).classList.add('active'); }
        async function fetchNotifs() { const r=await fetch('/api/notifications'); const d=await r.json(); document.getElementById('notif-list').innerHTML = d.map(n=>`<div class="notif-item p-3 cursor-pointer"><p class="text-xs font-bold text-blue-400 uppercase mb-1">${n.type}</p><p class="text-sm text-gray-200">${n.msg}</p></div>`).join(''); }
        function toggleNotifs() { document.getElementById('notif-dropdown').classList.toggle('hidden'); }
        function toggleChat() { document.getElementById('chat-window').classList.toggle('hidden'); }
        function handleChatKey(e) { if(e.key==='Enter') sendChat(); }
        async function sendChat() { const i=document.getElementById('chat-input'); const m=i.value.trim(); if(!m)return; const h=document.getElementById('chat-history'); h.innerHTML+=`<div class="chat-msg msg-user">${m}</div>`; i.value=""; h.scrollTop=h.scrollHeight; const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})}); const d=await r.json(); h.innerHTML+=`<div class="chat-msg msg-bot">${d.response}</div>`; h.scrollTop=h.scrollHeight; }
        
        async function init() {
            fetchNotifs();
            const dRes = await fetch('/api/dashboard-data'); const data = await dRes.json();
            document.getElementById('spots-list').innerHTML = data.spots.map(s => `<div class="bg-slate-800 p-5 rounded-xl hover:-translate-y-1 transition duration-300 border border-slate-700"><div class="flex justify-between items-start mb-2"><h3 class="font-bold text-xl text-orange-100">${s.name}</h3><span class="text-xs bg-orange-900/50 text-orange-200 px-2 py-1 rounded border border-orange-500/30">${s.distance}</span></div><p class="text-sm text-gray-400">Vibe: <span class="text-orange-400">${s.vibe}</span></p></div>`).join('');
            const mRes = await fetch('/api/mess-data'); globalMessMenu = await mRes.json();
            document.getElementById('mess-day-select').value = data.day in globalMessMenu ? data.day : "Monday"; updateMessDisplay();
            const tRes = await fetch('/api/timetable-data'); globalTimetable = await tRes.json();
            document.getElementById('timetable-day-select').value = (data.day in globalTimetable && globalTimetable[data.day].length > 0) ? data.day : "Monday"; updateTimetableDisplay();
        }
        function updateMessDisplay() { const d=document.getElementById('mess-day-select').value; const m=globalMessMenu[d]; if(m){ document.getElementById('mess-bf').innerText=m.Breakfast; document.getElementById('mess-lunch').innerText=m.Lunch; document.getElementById('mess-dinner').innerText=m.Dinner; } }
        function updateTimetableDisplay() { const d=document.getElementById('timetable-day-select').value; const c=globalTimetable[d]||[]; const l=document.getElementById('timetable-list'); const e=document.getElementById('no-classes-msg'); l.innerHTML=""; if(c.length===0){ e.classList.remove('hidden'); }else{ e.classList.add('hidden'); l.innerHTML=c.map(x=>`<div class="bg-slate-800 p-4 rounded-xl flex justify-between items-center hover:bg-slate-700 transition border-l-4 border-blue-500/50"><div><p class="font-bold text-lg text-white">${x.subject}</p><p class="text-sm text-blue-300 font-mono">${x.time}</p></div><span class="bg-slate-900 px-3 py-1 rounded text-sm text-gray-300 border border-slate-700">${x.room}</span></div>`).join(''); } }
        async function summarizeMail() { const b=document.getElementById('mail-btn'); const o=b.innerText; b.innerText="Processing AI..."; b.disabled=true; try{ const t=document.getElementById('mail-input').value; const r=await fetch('/api/mail-summary',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t})}); if(!r.ok) throw new Error(); const d=await r.json(); document.getElementById('mail-summary-text').innerText=d.summary; document.getElementById('mail-deadline').innerText=d.deadline; document.getElementById('ai-tags').innerHTML = `<span class="badge ${d.category==='Academic'?'bg-blue-600':'bg-gray-600'}">${d.category}</span>` + (d.priority==='High'?`<span class="badge bg-red-600 animate-pulse">🔥 URGENT</span>`:''); document.getElementById('mail-result-container').classList.remove('hidden'); }catch(e){alert("Error processing mail.");}finally{b.innerText=o;b.disabled=false;} }
        async function findItem() { const i=document.getElementById('lost-item').value; const r=await fetch('/api/lost-found',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({item:i})}); const d=await r.json(); const l=document.getElementById('lost-results'); if(d.matches.length>0){ l.innerHTML=d.matches.map(m=>`<div class="bg-green-900/30 border border-green-500 p-4 rounded-xl flex justify-between items-center animate-in"><div><p class="font-bold text-green-300">✅ Found: ${m.item}</p><p class="text-sm text-gray-400">Location: ${m.location}</p></div></div>`).join(''); }else{ l.innerHTML=`<div class="bg-slate-800 p-4 rounded-xl text-center text-gray-500">No matches found.</div>`; } }
        init();
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)