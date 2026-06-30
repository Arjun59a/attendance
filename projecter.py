import time, calendar, hashlib, qrcode, cv2, numpy as np

# DO NOT CHANGE THIS SALT
SECRET_SALT = "GanpatUniv_IT_Sem5_2026_SecureKey"

# [Start_Time, End_Time, Is_Running]
# 0 = Session Stopped (strictly bounded by time), 1 = Session Active (>)
sessions = [[0, 0, 1] for _ in range(20)] 
ACTIVE_SESSION_INDEX = 0 

def generate_qr():
    cv2.namedWindow("CLASSROOM ATTENDANCE GATEWAY", cv2.WINDOW_NORMAL)
    while True:
        curr = calendar.timegm(time.gmtime())
        bracket = curr // 3
        # Generate SHA-256 token
        token = hashlib.sha256(f"{SECRET_SALT}_{bracket}".encode()).hexdigest()[:16]
        
        # Get session details from buffer
        s = sessions[ACTIVE_SESSION_INDEX]
        # Payload: Token | SessionID | StartTime | EndTime | IsRunning
        qr_data = f"{token}|{ACTIVE_SESSION_INDEX}|{s[0]}|{s[1]}|{s[2]}"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        cv2.imshow("CLASSROOM ATTENDANCE GATEWAY", cv2.resize(np.array(img), (600, 600)))
        if cv2.waitKey(1000) & 0xFF == ord('q'): break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    generate_qr()