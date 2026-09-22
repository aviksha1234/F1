# 🏎️ F1 PIT STOP MASTER
> *"EVERY SECOND COUNTS."*

A fully functional, high-octane motorsport Python game built with **Pygame**. Experience the intensity of Formula 1 pit stops: race through dynamic circuits, react to the urgent `"BOX BOX BOX!"` radio command, and execute high-precision tyre changes against an adaptive AI crew.

---

## 🏁 Key Features

* **State-Machine Architecture (22 Distinct States)**:
  * Cinematic Lights-Out Intro with starting lights countdown and car launch
  * Responsive Main Menu with carbon-fiber styling, metallic panels, and sound effects
  * Car Selection with 4 fictional motorsport teams (Velocity Racing, Apex Motorsport, Redline GP, Titan Racing)
  * Difficulty Selection (EASY, MEDIUM, HARD, PRO)
  * 2.5D Interactive Circuit Racing with telemetry HUD, rival cars, track curves, and dynamic weather
  * Radio Callout (`"BOX BOX BOX!"`) with player reaction-time tracking
  * Pit Lane Entry & Animated Pit Box with Maya and crew
  * **5 Interactive Pit Stop Mini-Games**:
    1. **Wheel Nut Removal**: Sequential click pattern (FL → FR → RL → RR) with nut ejection and pneumatic audio
    2. **Fresh Tyre Installation**: Drag-and-drop mechanics with magnetic hub snapping
    3. **Pneumatic Wheel Gun Timing**: Oscillating sweet-spot timing bar (Red/Yellow/Green)
    4. **Front Wing Strategy**: Aerodynamic damage assessment (Change Wing vs. Keep Wing)
    5. **Green Light Pit Release**: Reaction timing to green lollipop with false-start detection (+0.50s unsafe release penalty)
  * Head-to-Head AI Comparison & Live Delta Display
  * Dynamic AI Race Engineer Analysis with tailored telemetry feedback
  * Workshop Garage with 5 upgradeable pit equipment systems
  * World Championship Mode across 5 fictional circuits
  * Persistent Global Leaderboard and Save System (`data/player.json`, `data/leaderboard.json`)
  * Full In-Game Pause Menu (ESC) & Settings Panel

* **Lead Tyre Engineer: Maya**:
  * Professional, sporty adult female lead mechanic with team jacket, fitted team apparel, racing boots, gloves, and team radio headset.
  * Fully animated procedural states: running to the car, kneeling beside the wheel, operating the pneumatic wheel gun, inspecting tyre wear, and giving the release signal.

* **Self-Contained Audio Synthesizer**:
  * Procedurally synthesized motorsport sound effects: engine revs, tire squeals, pneumatic wheel guns, team radio beeps, countdown beeps, metallic tyre locks, and crowd cheers.
  * Driving electronic motorsport synth music track.
  * Zero missing-file crashes.

---

## 🕹️ Controls

| Action | Keyboard | Mouse |
| :--- | :--- | :--- |
| **Accelerate** | `W` or `UP ARROW` | — |
| **Brake / Reverse** | `S` or `DOWN ARROW` | — |
| **Steer Left** | `A` or `LEFT ARROW` | — |
| **Steer Right** | `D` or `RIGHT ARROW` | — |
| **Confirm / Enter Pit / Lock / Release** | `SPACE` or `ENTER` | Left Click |
| **Tyre Mounting** | — | Click & Drag Tyre to Wheel Hub |
| **Wheel Nut Removal** | — | Click Wheel Hubs in Sequence |
| **Pause Game** | `ESCAPE` | — |
| **Toggle Music** | `M` | Settings Menu |
| **Toggle Sound Effects (SFX)** | `F1` | Settings Menu |

---

## 🚀 Installation & How to Run

### System Requirements
* Python 3.11+
* Windows, macOS, or Linux

### Quick Start (Windows)
Double-click `run.bat` or execute in PowerShell/CMD:
```powershell
.\run.bat
```

### Manual Run
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Launch the game:
```bash
python main.py
```

*(If using the provided virtual environment on Windows):*
### Web Browser Edition (Play via URL)
You can also launch and play directly in your web browser:
1. Start the local server:
```bash
python server.py
```
2. Open in your browser:
👉 **[http://localhost:8000](http://localhost:8000)**

---

## 🧠 Adaptive AI & Scoring Engine

### AI Pit Crew Difficulties
* **EASY**: ~3.00s base time
* **MEDIUM**: ~2.50s base time
* **HARD**: ~2.20s base time
* **PRO**: ~2.00s base time

### Adaptive Learning Engine
The AI continuously monitors your rolling average pit time. If you consistently outperform your selected difficulty target, the AI adapts its performance target to challenge your new skill level, notifying you on the comparison screen:
```text
🧠 AI ADAPTATION
Your recent avg: 2.21s.
AI has adapted to your skill level.
NEXT AI TARGET: 2.15s
```

### Pit Crew Rating (0–100 Score)
* **90–100**: ELITE CREW
* **75–89**: PROFESSIONAL
* **60–74**: ROOKIE
* **< 60**: NEED MORE PRACTICE

---

## 🔧 Garage Upgrades

Coins earned from races and pit stops can be spent in the Garage:
1. **Pneumatic Wheel Gun**: Widens the green sweet-spot timing window (+5% per level).
2. **Tyre Crew Synergy**: Expands magnetic snap radius when mounting fresh tyres (+12px per level).
3. **Quick-Lift Hydraulic Jack**: Reduces transition delay when lifting and lowering the chassis.
4. **Captive Nut System**: Minimizes penalty time for inaccurate wheel clicks.
5. **Pit Crew Conditioning**: Increases crew synchronization and overall score multiplier (+6% per level).

---

## 🏆 Championship Circuits

1. **Desert GP**: High heat, severe tyre degradation (25 laps).
2. **Neon City GP**: Night street circuit with illuminated barriers (30 laps).
3. **Coastal GP**: Sudden rain squalls requiring intermediate/wet tyre strategy (28 laps).
4. **Mountain GP**: Extreme elevation changes and heavy braking zones (26 laps).
5. **Grand Finale**: Pouring torrential rain showdown for the title (35 laps).

---

## 💾 Save System & Data Integrity

All progress is automatically saved to JSON files under the `data/` directory:
* `data/player.json`: Player name, coin balance, car selection, upgrade levels, career stats, and championship progress.
* `data/leaderboard.json`: Top 10 fastest pit stops, win/loss records, and average times.

The game features automatic file creation and corrupted-file recovery to ensure it never crashes if a file is missing or damaged.

---

## 🛡️ Troubleshooting

* **No audio / silent mode**: If no audio device is detected, the audio manager automatically runs in silent fallback mode without crashing.
* **Window scaling**: The game renders in standard 1280×720 (16:9) motorsport layout.
* **Dependencies**: Run `pip install pygame>=2.5.0`.
