import time
import calendar
import hashlib
import qrcode
import cv2
import numpy as np

# This is the secret key that links the Broadcaster and the Google Script
SECRET_SALT = "GanpatUniv_IT_Sem5_2026_SecureKey"

# Expanded Buffer: [Start_Time_Epoch, End_Time_Epoch, Is_Running_Status]
# We initialize all 20 sessions explicitly
sessions = []
for i in range(20):
    sessions.append([0, 0, 1]) 

ACTIVE_SESSION_INDEX = 0 

def generate_qr():
    # Set window to a fixed size for better stability during presentation
    cv2.namedWindow("CLASSROOM ATTENDANCE GATEWAY", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("CLASSROOM ATTENDANCE GATEWAY", 600, 600)
    
    while True:
        # Get current GMT time for synchronization
        current_time_epoch = calendar.timegm(time.gmtime())
        current_bracket = current_time_epoch // 3
        
        # Create the token using SHA-256
        raw_message = (SECRET_SALT + "_" + str(current_bracket)).encode('utf-8')
        secure_token = hashlib.sha256(raw_message).hexdigest()[:16]
        
        # Retrieve the specific session configuration from our buffer
        active_session = sessions[ACTIVE_SESSION_INDEX]
        start_time = active_session[0]
        end_time = active_session[1]
        is_running_status = active_session[2]
        
        # The QR Payload (The "Passport" of the attendance)
        qr_data = f"{secure_token}|{ACTIVE_SESSION_INDEX}|{start_time}|{end_time}|{is_running_status}"
        
        # Generate the QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Convert to OpenCV image format
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        opencv_img = cv2.cvtColor(np.array(qr_img), cv2.COLOR_RGB2BGR)
        
        cv2.imshow("CLASSROOM ATTENDANCE GATEWAY", opencv_img)
        
        # Refresh every 1000ms, break if 'q' is pressed
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break
            
    cv2.destroyAllWindows()

if __name__ == "__main__":
    generate_qr()