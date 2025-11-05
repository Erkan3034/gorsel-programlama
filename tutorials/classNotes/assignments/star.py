import time

def print_star_pattern(n):
    # Increasing pattern
    for i in range(1, n + 1):
        print("* " * i)
        time.sleep(0.1)
    
    # Decreasing pattern
    for i in range(n - 1, 0, -1):
        print("* " * i)
        time.sleep(0.1)
    
# Get input from user
n = int(input("Yıldız satırı uzunluğunu giriniz: "))

while True:
    print_star_pattern(n)
