import hashlib
import json
import time
import os
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
import qrcode
from qrcode.constants import ERROR_CORRECT_H

SECRET_SALT = "CHANGE_ME_TO_A_LONG_RANDOM_SECRET"
BRACKET_SECONDS = 3

APPS_SCRIPT_URL = "YOUR_APPS_SCRIPT_WEB_APP_URL_HERE"

OUTPUT_FILE = "attendance_qr.png"
WAITING_FILE = "attendance_qr_waiting.png"

POLL_SECONDS = 5
QR_TICK_SECONDS = 0.10

QR_BOX_SIZE = 32
QR_BORDER = 4

def fetch_active_session():
    url = APPS_SCRIPT_URL + "?" + urllib.parse.urlencode({"action": "getActiveSession"})
    try:
        with urllib.request.urlopen(url, timeout=10) as res:
            data = json.loads(res.read().decode("utf-8"))
    except Exception as e:
        print("Could not reach server:", e)
        return None

    if not data.get("ok") or not data.get("active"):
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
        SECRET_SALT,
        str(bracket),
        session["id"],
        session["start"],
        session["end"],
        session["running"]
    ])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

def payload_for(session):
    return "|".join([
        token_for(session, current_bracket()),
        session["id"],
        session["start"],
        session["end"],
        session["running"]
    ])

def write_qr(payload, filename=OUTPUT_FILE):
    qr = qrcode.QRCode(
        error_correction=ERROR_CORRECT_H,
        box_size=QR_BOX_SIZE,
        border=QR_BORDER
    )
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    temp_file = filename + ".tmp.png"
    img.save(temp_file)
    os.replace(temp_file, filename)

def write_waiting_image():
    write_qr("NO_ACTIVE_SESSION", WAITING_FILE)

def india_time_str(iso_utc_str):
    dt = datetime.strptime(iso_utc_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return (dt + timedelta(hours=5, minutes=30)).strftime("%d-%m-%Y %I:%M:%S %p")

print("Waiting for faculty session...")
active_session = None
last_polled = 0
last_payload = ""

while True:
    now = time.time()

    if now - last_polled >= POLL_SECONDS:
        last_polled = now
        found = fetch_active_session()

        if found and (
            not active_session
            or found["id"] != active_session["id"]
            or found["start"] != active_session["start"]
        ):
            active_session = found
            last_payload = ""
            print(
                "Active:",
                active_session["id"],
                active_session["className"],
                active_session["lectureType"],
                india_time_str(active_session["start"])
            )

        elif not found and active_session:
            print("Session ended. Waiting...")
            active_session = None
            write_waiting_image()
            last_payload = ""

    if active_session:
        payload = payload_for(active_session)
        if payload != last_payload:
            write_qr(payload)
            print("QR updated:", payload)
            last_payload = payload
    else:
        if last_payload != "WAITING":
            write_waiting_image()
            last_payload = "WAITING"

    time.sleep(QR_TICK_SECONDS)