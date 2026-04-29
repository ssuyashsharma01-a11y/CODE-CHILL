// --- ⚙️ PRODUCTION JS ---
let socket;
const VIDEO = document.getElementById('video');
const CANVAS = document.createElement('canvas'); 
const ctx = CANVAS.getContext('2d');

function connect() {
    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    socket = new WebSocket(protocol + window.location.host + '/ws/attendance');

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const statusBox = document.querySelector('.scanner-box');
        
        document.getElementById('status-text').innerText = data.status;
        document.getElementById('challenge-node').innerText = data.challenge || "---";
        
        // Audit Fix #10: Progress logic
        if (data.progress !== undefined) {
            document.getElementById('progress-fill').style.width = data.progress + "%";
        }

        // Visual Feedback (Colors)
        if (data.status === "SUCCESS") statusBox.style.borderColor = "#00ff88";
        else if (data.status === "COOLDOWN") statusBox.style.borderColor = "#ffcc00";
        else if (data.status === "NO_FACE") statusBox.style.borderColor = "#ff4444";
        
        if (data.name) document.getElementById('user-name').innerText = data.name;
    };

    socket.onclose = () => {
        console.log("⚠️ Connection Lost. Reconnecting...");
        setTimeout(connect, 2000);
    };
}

// PERFORMANCE: Resize & Compress
setInterval(() => {
    if (socket && socket.readyState === WebSocket.OPEN && VIDEO.readyState === 4) {
        // Only process if tab is active (Performance Fix)
        if (document.visibilityState === 'visible') {
            CANVAS.width = 320; 
            CANVAS.height = 240;
            ctx.drawImage(VIDEO, 0, 0, 320, 240);
            socket.send(CANVAS.toDataURL('image/jpeg', 0.4));
        }
    }
}, 450);

// Camera Init with UI Feedback
navigator.mediaDevices.getUserMedia({ video: true })
    .then(s => VIDEO.srcObject = s)
    .catch(() => alert("CRITICAL: Camera access denied. Attendance disabled."));

connect();

// Function to eliminate (delete) a notice
async function eliminateNotice(button) {
    const noticeId = button.getAttribute('data-id');
    if (!noticeId) {
        console.error('Delete failed: missing notice ID', button);
        return alert('Deletion protocol failed: missing notice ID.');
    }
    if (!confirm('Are you sure you want to delete this notice?')) return;

    try {
        const response = await fetch(`/api/v1/admin/notice/${encodeURIComponent(noticeId)}`, {
            method: 'DELETE'
        });
        if (response.ok) {
            button.closest('.relative.group').remove();
        } else {
            console.error('Delete failed:', response.status, response.statusText);
            alert(`Failed to delete notice: ${response.status} ${response.statusText}`);
        }
    } catch (error) {
        console.error('Error deleting notice:', error);
        alert('Error deleting notice: network error.');
    }
}