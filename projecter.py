import hashlib
import time
from datetime import datetime, timezone
import qrcode

SECRET_SALT = "CHANGE_ME_TO_A_LONG_RANDOM_SECRET"
BRACKET_SECONDS = 3
OUTPUT_FILE = "attendance_qr.png"

SESSIONS = [
    {
        "id": "CLASS-01",
        "start": "2026-06-30T00:00:00Z",
        "end": "2026-07-01T23:59:59Z",
        "running": "0"
    }
]

ACTIVE_SESSION_INDEX = 0

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

last = ""
session = SESSIONS[ACTIVE_SESSION_INDEX]

print("Broadcasting:", session["id"])
print("QR file:", OUTPUT_FILE)

while True:
    payload = payload_for(session)
    if payload != last:
        write_qr(payload)
        print("QR updated:", payload)
        last = payload
    time.sleep(0.25)