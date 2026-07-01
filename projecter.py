import hashlib
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
import qrcode

# ---- must match script.gs exactly ----
SECRET_SALT = "CHANGE_ME_TO_A_LONG_RANDOM_SECRET"
BRACKET_SECONDS = 3

# Paste the SAME Apps Script URL used in portal.html / faculty.html
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz8ONnxPB1_Lx2btLyQFcBNDPWFZp9sa94OC5JtsMXRykJ614mmUDJQNbJWEr2feotfZA/exec"

OUTPUT_FILE = "attendance_qr.png"
WAITING_FILE = "attendance_qr_waiting.png"

POLL_SECONDS = 5          # how often to ask the sheet "who is running right now"
QR_TICK_SECONDS = 0.25    # how often to check if the QR needs refreshing


def fetch_active_session():
    """Ask script.gs which session is currently RUNNING. Returns dict or None."""
    url = APPS_SCRIPT_URL + "?" + urllib.parse.urlencode({"action": "getActiveSession"})
    try:
        with urllib.request.urlopen(url, timeout=10) as res:
            data = json.loads(res.read().decode("utf-8"))
    except Exception as e:
        print("Could not reach the server:", e)
        return None

    if not data.get("ok"):
        print("Server error:", data.get("message"))
        return None

    if not data.get("active"):
        return None

    return {
        "id": data["sessionId"],
        "start": data["startTime"],
        "end": data.get("endTime", ""),
        "running": "1",
        "className": data.get("className", ""),
        "lectureType": data.get("lectureType", "")
    }


def current_bracket():
    return int(datetime.now(timezone.utc).timestamp()) // BRACKET_SECONDS


def token_for(session, bracket):
    raw = "|".join([
        SECRET_SALT, str(bracket), session["id"],
        session["start"], session["end"], session["running"]
    ])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def payload_for(session):
    return "|".join([
        token_for(session, current_bracket()),
        session["id"], session["start"], session["end"], session["running"]
    ])


def write_qr(payload, filename=OUTPUT_FILE):
    qrcode.make(payload).save(filename)


def write_waiting_image():
    qrcode.make("NO_ACTIVE_SESSION").save(WAITING_FILE)


def india_time_str(iso_utc_str):
    dt = datetime.strptime(iso_utc_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return (dt + timedelta(hours=5, minutes=30)).strftime("%d-%m-%Y %I:%M:%S %p")


print("Waiting for faculty to start a session...")
print("Polling:", APPS_SCRIPT_URL)

active_session = None
last_polled = 0
last_payload = ""

while True:
    now = time.time()

    if now - last_polled >= POLL_SECONDS:
        last_polled = now
        found = fetch_active_session()

        if found and (not active_session or found["id"] != active_session["id"] or found["start"] != active_session["start"]):
            active_session = found
            last_payload = ""
            print("Active session found:", active_session["id"],
                  "-", active_session["className"], "-", active_session["lectureType"],
                  "- started", india_time_str(active_session["start"]))

        elif not found and active_session:
            print("Session ended or no longer running. Waiting for next session...")
            active_session = None
            write_waiting_image()
            last_payload = ""

        elif not found and not active_session:
            # still nothing running, keep the waiting image up
            pass

    if active_session:
        payload = payload_for(active_session)
        if payload != last_payload:
            write_qr(payload)
            print("QR updated:", payload)
            last_payload = payload
    else:
        # no active session yet — waiting image already written when we detected the change
        if last_payload != "WAITING":
            write_waiting_image()
            last_payload = "WAITING"

    time.sleep(QR_TICK_SECONDS)