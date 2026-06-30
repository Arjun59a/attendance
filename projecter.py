import hashlib
import time
from datetime import datetime, timezone, timedelta
import qrcode

SECRET_SALT = "CHANGE_ME_TO_A_LONG_RANDOM_SECRET"
BRACKET_SECONDS = 3
OUTPUT_FILE = "attendance_qr.png"

SESSION_ID = "CLASS-01"
CLASS_DURATION_MINUTES = 60

session_start = datetime.now(timezone.utc)
session_end = session_start + timedelta(minutes=CLASS_DURATION_MINUTES)

SESSION = {
    "id": SESSION_ID,
    "start": session_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "end": session_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "running": "0"
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
        session["running"],
    ])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

def payload_for(session):
    return "|".join([
        token_for(session, current_bracket()),
        session["id"],
        session["start"],
        session["end"],
        session["running"],
    ])

def write_qr(payload):
    img = qrcode.make(payload)
    img.save(OUTPUT_FILE)

def india_time(dt):
    return (dt + timedelta(hours=5, minutes=30)).strftime("%d-%m-%Y %I:%M:%S %p")

print("Session ID:", SESSION_ID)
print("Session started UTC:", SESSION["start"])
print("Session ends UTC:", SESSION["end"])
print("India start time:", india_time(session_start))
print("India end time:", india_time(session_end))
print("QR file:", OUTPUT_FILE)

last = ""

while True:
    payload = payload_for(SESSION)
    if payload != last:
        write_qr(payload)
        print("QR updated:", payload)
        last = payload
    time.sleep(0.25)