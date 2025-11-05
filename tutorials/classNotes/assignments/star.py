import time

def print_star_pattern(n):
    # artan desen
    for i in range(1, n + 1):
        print("* " * i)
        time.sleep(0.1)
    
    # azalan desen
    for i in range(n - 1, 0, -1): #n-1 den 1 e kadar azalan
        print("* " * i)
        time.sleep(0.1)
    
# kullanıcıdan girdi al
n = int(input("Yıldız satırı uzunluğunu giriniz: "))

while True:
    print_star_pattern(n)
