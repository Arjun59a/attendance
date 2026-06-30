import time, calendar, hashlib, qrcode, cv2, numpy as np

SECRET_SALT = "GanpatUniv_IT_Sem5_2026_SecureKey"
# Buffer: [Start_Time_Epoch, End_Time_Epoch, Is_Running]
sessions = [[0, 0, 0] for _ in range(20)] 
ACTIVE_SESSION_INDEX = 0 

def generate_qr():
    cv2.namedWindow("3-Sec Attendance", cv2.WINDOW_NORMAL)
    while True:
        curr = calendar.timegm(time.gmtime())
        bracket = curr // 3
        # Hash the salt and current bracket
        token = hashlib.sha256(f"{SECRET_SALT}_{bracket}".encode()).hexdigest()[:16]
        
        # QR Payload: Token | SessionID | StartTime
        s = sessions[ACTIVE_SESSION_INDEX]
        qr_data = f"{token}|{ACTIVE_SESSION_INDEX}|{s[0]}"
        
        qr = qrcode.make(qr_data)
        cv2.imshow("3-Sec Attendance", cv2.cvtColor(np.array(qr.convert('RGB')), cv2.COLOR_RGB2BGR))
        if cv2.waitKey(1000) & 0xFF == ord('q'): break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    generate_qr()