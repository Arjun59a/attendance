import time
import os
import hashlib
import qrcode
from datetime import datetime

SECRET_SALT = "GanpatUniv_IT_Sem5_2026_SecureKey"
TIME_WINDOW_SECONDS = 3  # The strict 3-second network token expiry threshold

def generate_secure_token():
    current_bracket = int(time.time() // TIME_WINDOW_SECONDS)
    raw_string = f"{SECRET_SALT}_{current_bracket}"
    secure_hash = hashlib.sha256(raw_string.encode()).hexdigest()
    return secure_hash[:16]

print("🚀 Dynamic 3-Second Classroom QR Projector Active.")
print("Press Ctrl + C to terminate cleanly.")

try:
    while True:
        token = generate_secure_token()
        current_time = datetime.now().strftime("%H:%M:%S")
        
        qr = qrcode.QRCode(version=1, box_size=15, border=3)
        qr.add_data(token)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("attendance_qr.png")
        
        print(f"[{current_time}] Live Token: {token} -> Syncing structural output to (attendance_qr.png)")
        time.sleep(TIME_WINDOW_SECONDS)

except KeyboardInterrupt:
    print("\n🛑 Local loop terminated successfully.")