from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from coordinator import Coordinator

app = FastAPI()
coordinator = Coordinator()

# Request model
class ChatRequest(BaseModel):
    message: str

# Response model
class ChatResponse(BaseModel):
    response: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    user_msg = req.message.lower()

    # ----------------------------------
    # 1️⃣ Handle pilot status update
    # ----------------------------------
    if "mark" in user_msg or "set" in user_msg or "update" in user_msg:
        words = user_msg.replace(",", "").split()

        # Extract pilot name
        if "mark" in words:
            pilot_name = words[words.index("mark") + 1].capitalize()
        elif "set" in words:
            pilot_name = words[words.index("set") + 1].capitalize()
        elif "update" in words:
            pilot_name = words[words.index("update") + 1].capitalize()
        else:
            pilot_name = None

        # Extract status
        if "on leave" in user_msg:
            new_status = "On Leave"
        elif "available" in user_msg:
            new_status = "Available"
        elif "assigned" in user_msg:
            new_status = "Assigned"
        elif "unavailable" in user_msg:
            new_status = "Unavailable"
        else:
            new_status = None

        if not pilot_name or not new_status:
            return {
                "response": "Could not understand pilot name or status. Try: 'Mark Sneha as Available'."
            }

        result = coordinator.update_pilot_status(pilot_name, new_status)

        if "error" in result:
            return {"response": result["error"]}

        return {"response": result["success"]}
    
    # ----------------------------------
    # 🚨 Urgent reassignment
    # ----------------------------------
    if "urgent" in user_msg or "reassign" in user_msg:
        result = coordinator.urgent_reassignment(user_msg)

        if "error" in result:
            return {"response": result["error"]}

        return {
            "response": (
                f"Urgent reassignment completed. "
                f"Pilot {result['pilot']} reassigned from "
                f"{result['previous_assignment']} to mission "
                f"{result['urgent_mission']} in {result['new_location']}."
            )
        }


    # ----------------------------------
    # 2️⃣ Handle assignment requests
    # ----------------------------------
    if "assign" in user_msg:
        result = coordinator.recommend_assignment(user_msg)

        if "error" in result:
            return {"response": result["error"]}

        return {
            "response": (
                f"Mission {result['mission']} in {result['location']}: "
                f"{len(result['pilots'])} pilots and "
                f"{len(result['drones'])} drones available"
            )
        }

    # ----------------------------------
    # 3️⃣ Default response
    # ----------------------------------
    return {
        "response": "I can help with pilot status updates, assignments, conflicts, and urgent reassignments."
    }


@app.get("/", response_class=HTMLResponse)
def ui():
        return """
        <!doctype html>
        <html lang="en">
            <head>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width,initial-scale=1" />
                <title>Skylark Drone Ops</title>
                <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
                <style>
                    :root{
                        --bg:#0f1724;--card:#0b1220;--accent:#0ea5a4;--muted:#9aa4b2;--glass:rgba(255,255,255,0.04)
                    }
                    html,body{height:100%;margin:0;font-family:Inter,system-ui,Segoe UI,Roboto,Arial;color:#e6eef6;background:linear-gradient(180deg,#071029 0%, #071a2b 60%)}
                    .nav{display:flex;align-items:center;gap:12px;padding:18px 36px}
                    .logo{display:flex;align-items:center;gap:12px}
                    .logo .mark{width:44px;height:44px;border-radius:10px;background:linear-gradient(135deg,var(--accent),#1fb6b9);display:flex;align-items:center;justify-content:center;font-weight:700;color:#012;box-shadow:0 6px 20px rgba(14,165,164,0.12)}
                    .brand{font-weight:700;font-size:18px}

                    .container{max-width:1100px;margin:28px auto;padding:28px}
                    .hero{display:flex;gap:28px;align-items:center}
                    .hero-card{flex:1;background:linear-gradient(180deg, rgba(255,255,255,0.02), var(--glass));padding:28px;border-radius:14px;box-shadow:0 8px 30px rgba(2,6,23,0.6)}
                    .hero h1{margin:0 0 12px;font-size:28px}
                    .hero p{color:var(--muted);margin:0 0 18px}

                    .chat-panel{width:420px;background:linear-gradient(180deg,#071423 0%, #071827 60%);border-radius:12px;padding:16px;border:1px solid rgba(255,255,255,0.03)}
                    .history{height:360px;overflow:auto;padding:12px;display:flex;flex-direction:column;gap:8px}
                    .msg{max-width:84%;padding:10px 12px;border-radius:12px;font-size:14px;line-height:1.3}
                    .msg.user{align-self:flex-end;background:linear-gradient(90deg,var(--accent),#2dd4bf);color:#042025}
                    .msg.bot{align-self:flex-start;background:rgba(255,255,255,0.03);color:var(--muted)}
                    .controls{display:flex;gap:8px;margin-top:12px}
                    .controls input[type=text]{flex:1;padding:10px;border-radius:8px;border:1px solid rgba(255,255,255,0.04);background:transparent;color:inherit}
                    .btn{background:var(--accent);border:none;color:#012;padding:10px 14px;border-radius:8px;cursor:pointer;font-weight:600}
                    .btn.ghost{background:transparent;border:1px solid rgba(255,255,255,0.04);color:var(--muted)}

                    footer{margin-top:18px;color:var(--muted);font-size:13px}
                    @media(max-width:900px){.hero{flex-direction:column}.chat-panel{width:100%}}
                </style>
            </head>
            <body>
                <nav class="nav">
                    <div class="logo">
                        <div class="mark">SK</div>
                        <div>
                            <div class="brand">Skylark Drone Ops</div>
                            <div style="font-size:12px;color:var(--muted)">Operations & Assignment Assistant</div>
                        </div>
                    </div>
                </nav>

                <main class="container">
                    <div class="hero">
                        <section class="hero-card">
                            <h1>Assistant for Pilot & Drone Assignments</h1>
                            <p>Ask the assistant to assign pilots and drones, update pilot status, or perform urgent reassignments. Example commands: <em>Assign PRJ001</em>, <em>Mark Sneha as Available</em>.</p>
                            <div style="display:flex;gap:14px;margin-top:18px">
                                <div style="flex:1">
                                    <label style="display:block;margin-bottom:6px;color:var(--muted)">Enter message or command</label>
                                    <input id="msg" type="text" placeholder="e.g. assign PRJ001 or mark Sneha available" style="width:100%;padding:12px;border-radius:10px;border:1px solid rgba(255,255,255,0.03);background:transparent;color:inherit" />
                                </div>
                                <div style="display:flex;flex-direction:column;gap:8px">
                                    <button class="btn" id="send">Send</button>
                                    <button class="btn ghost" id="assign">Ask Assignment</button>
                                </div>
                            </div>
                            <footer>Built for internal operations • Data from Google Sheets</footer>
                        </section>

                        <aside class="chat-panel">
                            <div class="history" id="history"></div>
                            <div class="controls">
                                <input id="mini" type="text" placeholder="Type a quick command…" />
                                <button class="btn" id="miniSend">Go</button>
                            </div>
                        </aside>
                    </div>
                </main>

                <script>
                    const historyEl = document.getElementById('history');
                    function append(kind, text){
                        const d = document.createElement('div');
                        d.className = 'msg ' + (kind === 'user' ? 'user' : 'bot');
                        d.textContent = text;
                        historyEl.appendChild(d);
                        historyEl.scrollTop = historyEl.scrollHeight;
                    }

                    async function sendMessage(text){
                        if(!text) return;
                        append('user', text);
                        try{
                            const res = await fetch('/chat', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text})});
                            const j = await res.json();
                            append('bot', j.response || JSON.stringify(j));
                        }catch(e){
                            append('bot', 'Error: ' + (e.message || e));
                        }
                    }

                    document.getElementById('send').addEventListener('click', ()=>{
                        const v = document.getElementById('msg').value || '';
                        sendMessage(v);
                    });
                    document.getElementById('assign').addEventListener('click', ()=>{
                        const v = document.getElementById('msg').value || '';
                        sendMessage(v.includes('assign') ? v : `assign ${v}`);
                    });
                    document.getElementById('miniSend').addEventListener('click', ()=>{
                        const v = document.getElementById('mini').value || '';
                        sendMessage(v);
                    });
                    document.getElementById('msg').addEventListener('keydown',(e)=>{ if(e.key==='Enter') document.getElementById('send').click(); });
                    document.getElementById('mini').addEventListener('keydown',(e)=>{ if(e.key==='Enter') document.getElementById('miniSend').click(); });
                </script>
            </body>
        </html>
        """
