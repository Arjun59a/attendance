import time
import calendar
import hashlib
import qrcode
import cv2
import numpy as np

SECRET_SALT = "GanpatUniv_IT_Sem5_2026_SecureKey"
TIME_WINDOW_SECONDS = 1200  # 20 Minutes expiry

def live_qr_broadcaster():
    cv2.namedWindow("CLASSROOM ATTENDANCE GATEWAY", cv2.WINDOW_NORMAL)
    while True:
        current_epoch = calendar.timegm(time.gmtime())
        current_bracket = current_epoch // TIME_WINDOW_SECONDS
        
        # Raw message construction
        raw_message = (SECRET_SALT + "_" + str(current_bracket)).encode('utf-8')
        secure_token = hashlib.sha256(raw_message).hexdigest()[:16]
        
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(secure_token)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        opencv_img = cv2.cvtColor(np.array(qr_img), cv2.COLOR_RGB2BGR)
        
        cv2.imshow("CLASSROOM ATTENDANCE GATEWAY", cv2.resize(opencv_img, (600, 600)))
        if cv2.waitKey(1000) & 0xFF == ord('q'): break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    live_qr_broadcaster()