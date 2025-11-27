import pyautogui
import time
import keyboard

time.sleep(1)  # 3 saniye bekle, WhatsApp sekmesine geç

mesaj = "Selam! Bu mesaj otomatik gönderildi :)"

for i in range(1):  
    pyautogui.typewrite(mesaj)
    pyautogui.press("enter")
    time.sleep(1)
