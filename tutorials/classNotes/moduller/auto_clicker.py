import mouse
import time
import keyboard
print("Tıklama 10 saniye sonra başlayacak...")

# Geri sayım
for i in range(10, 0, -1):
    print(i)
    time.sleep(1)

print("Tıklama başladı!")

# 100 kez tıklama
for i in range(100):

    if keyboard.is_pressed("up"):
        print("Durdu!")
        break
    else:
        mouse.click()
        print(f"{i+1}. tıklama yapıldı")
        time.sleep(0.1)  # çok hızlı olmaması için ekledim
