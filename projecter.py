import time
import hashlib
import qrcode
import cv2
import numpy as np

# 🟢 CONFIGURATION SETTINGS
# Replace this string with your live production GitHub Pages URL
GITHUB_PORTAL_URL = "https://arjunthakor.github.io/smart-attendance/portal.html"
SECRET_SALT = "GanpatUniv_IT_Sem5_2026_SecureKey"
TIME_WINDOW_SECONDS = 3

def generate_secure_embedded_url(faculty_script_url):
    current_epoch = int(time.time())
    current_bracket = current_epoch // TIME_WINDOW_SECONDS
    
    # Generate the 3-second secure token sequence
    raw_message = f"{SECRET_SALT}_{current_bracket}".encode('utf-8')
    secure_token = hashlib.sha256(raw_message).hexdigest()[:16]
    
    # Embed parameters cleanly into a single unified routing path
    dynamic_student_link = f"{GITHUB_PORTAL_URL}?rpc={faculty_script_url}&token={secure_token}"
    return dynamic_student_link

def live_qr_broadcaster(faculty_script_url):
    print("🚀 Smart Attendance Core Matrix Active...")
    print("📺 Broadcasting real-time routing payloads onto projector framework...")
    
    cv2.namedWindow("CLASSROOM ATTENDANCE GATEWAY", cv2.WINDOW_NORMAL)
    
    while True:
        target_payload_url = generate_secure_embedded_url(faculty_script_url)
        
        # Build out the visual QR pixel block matrix 
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(target_payload_url)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        opencv_img = cv2.cvtColor(np.array(qr_img), cv2.COLOR_RGB2BGR)
        
        display_frame = cv2.resize(opencv_img, (600, 600))
        cv2.imshow("CLASSROOM ATTENDANCE GATEWAY", display_frame)
        
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    # The Apps Script deployment link copied from the Google Spreadsheet
    ACTIVE_FACULTY_EXEC_URL = "https://script.google.com/macros/s/AKfycbwW2TP9sig_QQCBgDaLC5Jc5PMy5Ll6Us6sDt-pxj-zaK8uVizk2Irzf5XVsMwlNq4vyg/exec"
    live_qr_broadcaster(ACTIVE_FACULTY_EXEC_URL)