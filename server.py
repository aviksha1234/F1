"""Local web server for F1 Pit Stop Master browser edition with REST API."""
import os
import sys
import json
import re
import http.server

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
DATA_DIR = os.path.join(BASE_DIR, "data")
LEADERBOARD_FILE = os.path.join(DATA_DIR, "leaderboard.json")
PLAYER_FILE = os.path.join(DATA_DIR, "player.json")

def sanitize_name(name):
    """Sanitizes player name for leaderboard storage."""
    if not name or not isinstance(name, str):
        return "DRIVER"
    cleaned = re.sub(r'[^A-Za-z0-9 _-]', '', name).strip().upper()
    return cleaned[:12] if cleaned else "DRIVER"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def log_message(self, format, *args):
        pass

    def _send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        # 1. API: Get Leaderboard
        if self.path == "/api/leaderboard":
            try:
                if os.path.exists(LEADERBOARD_FILE):
                    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                        data = json.load(f)
                else:
                    data = []
                self._send_json(200, data)
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        # 2. API: Get Player Progress
        if self.path.startswith("/api/progress"):
            try:
                if os.path.exists(PLAYER_FILE):
                    with open(PLAYER_FILE, "r", encoding="utf-8") as f:
                        data = json.load(f)
                else:
                    data = {"coins": 1500, "upgrades": {}}
                self._send_json(200, data)
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        # Static files
        super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

        try:
            payload = json.loads(post_data)
        except Exception:
            payload = {}

        # 1. API: Submit Leaderboard Entry
        if self.path == "/api/leaderboard":
            try:
                name = sanitize_name(payload.get("name", "DRIVER"))
                fastest_pit = float(payload.get("fastestPit", 99.99))
                avg_pit = float(payload.get("avgPit", fastest_pit))
                score = int(payload.get("score", 0))
                wins = int(payload.get("wins", 0))
                ai_wins = int(payload.get("aiWins", 0))

                entries = []
                if os.path.exists(LEADERBOARD_FILE):
                    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                        entries = json.load(f)

                # Check existing driver entry
                found = False
                for entry in entries:
                    if entry.get("name", "").upper() == name:
                        entry["fastest_pit"] = round(min(entry.get("fastest_pit", 99.99), fastest_pit), 2)
                        entry["average_pit"] = round(min(entry.get("average_pit", avg_pit), avg_pit), 2)
                        entry["best_score"] = max(entry.get("best_score", 0), score)
                        entry["player_wins"] = wins
                        entry["ai_wins"] = ai_wins
                        found = True
                        break

                if not found:
                    entries.append({
                        "name": name,
                        "fastest_pit": round(fastest_pit, 2),
                        "average_pit": round(avg_pit, 2),
                        "best_score": score,
                        "player_wins": wins,
                        "ai_wins": ai_wins
                    })

                entries.sort(key=lambda x: x.get("fastest_pit", 99.99))
                entries = entries[:10]

                with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
                    json.dump(entries, f, indent=2)

                self._send_json(200, {"status": "ok", "leaderboard": entries})
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        # 2. API: Save Player Progress
        if self.path.startswith("/api/progress"):
            try:
                existing = {}
                if os.path.exists(PLAYER_FILE):
                    with open(PLAYER_FILE, "r", encoding="utf-8") as f:
                        existing = json.load(f)

                # Merge allowed fields
                for k in ["name", "coins", "selected_car_id", "difficulty", "upgrades", "stats", "championship"]:
                    if k in payload:
                        existing[k] = payload[k]

                if "name" in existing:
                    existing["name"] = sanitize_name(existing["name"])

                with open(PLAYER_FILE, "w", encoding="utf-8") as f:
                    json.dump(existing, f, indent=2)

                self._send_json(200, {"status": "ok", "player": existing})
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        # 3. API: Clean Game Exit
        if self.path == "/api/exit":
            self._send_json(200, {"status": "shutting_down", "message": "Game application terminated safely."})
            def shutdown():
                import time
                time.sleep(0.6)
                os._exit(0)
            import threading
            threading.Thread(target=shutdown, daemon=True).start()
            return

        self._send_json(404, {"error": "Endpoint not found"})

def run_server():
    os.chdir(WEB_DIR)
    with http.server.ThreadingHTTPServer(("", PORT), CustomHandler) as httpd:
        print("=======================================================")
        print("   F1 PIT STOP MASTER 3D - MULTI-THREADED API SERVER")
        print(f"   URL: http://localhost:{PORT}")
        print("   API: /api/leaderboard | /api/progress/:id")
        print("=======================================================")
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    run_server()
