import time
import os

def asal_mi():
    # Eğer progress.txt varsa kaldığımız yeri oku
    if os.path.exists("progress.txt"):
        with open("progress.txt", "r", encoding="utf-8") as p:
            start = int(p.read().strip())
    else:
        start = 2  # ilk kez çalışıyorsa

    print(f"Başlangıç noktası: {start}")

    try:
        with open("primes_safe.txt", "a", encoding="utf-8") as dosya:
            for i in range(start, 1001):
                asal = True
                for j in range(2, int(i**0.5) + 1):
                    if i % j == 0:
                        asal = False
                        break

                if asal:
                    time.sleep(0.3)  # yavaşlatma
                    dosya.write(str(i) + "\n")
                    print("Asal bulundu:", i)

                # Her adımda progress.txt'yi güncelle
                with open("progress.txt", "w", encoding="utf-8") as p:
                    p.write(str(i + 1))

    except KeyboardInterrupt:
        print("\nCtrl+C ile durduruldu. İlerleme kaydedildi.")
        return

    print("\nİşlem tamamlandı. Tüm sayılar tarandı.")


asal_mi()