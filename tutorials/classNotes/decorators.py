# DECORATORS (Süsleyiciler)
"""
Decorator'lar fonksiyonları veya sınıfları değiştiren/kapsayan fonksiyonlardır.
Mevcut bir fonksiyona özellik eklemek istediğimizde kullanışlıdır.
"""

# ==========================================
# 1. TEMEL KULLANIM - @decorator_name
# ==========================================

def my_decorator(func):
    """Basit bir decorator örneği"""
    def wrapper():
        print("Fonksiyon çalışmadan önce...")
        func()
        print("Fonksiyon çalıştıktan sonra...")
    return wrapper

@my_decorator
def say_hello():
    print("Merhaba!")

# Kullanım:
# say_hello()
# Çıktı:
# Fonksiyon çalışmadan önce...
# Merhaba!
# Fonksiyon çalıştıktan sonra...

# ==========================================
# 2. ZAMANLAMA DECORATOR'I
# ==========================================

import time

def timing_decorator(func):
    """Fonksiyonun çalışma süresini ölçer"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} {end_time - start_time:.4f} saniye sürdü")
        return result
    return wrapper

@timing_decorator
def slow_function():
    time.sleep(1)
    print("İşlem tamamlandı!")

# slow_function()
# Çıktı: İşlem tamamlandı!
#        slow_function 1.0005 saniye sürdü

# ==========================================
# 3. PARAMETRE ALAN DECORATOR
# ==========================================

def repeat(num_times):
    """Fonksiyonu belirtilen kadar tekrarlar"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(num_times=3)
def greet(name):
    print(f"Merhaba {name}")

# greet("Ali")
# Çıktı:
# Merhaba Ali
# Merhaba Ali
# Merhaba Ali

# ==========================================
# 4. SINIFLAR İÇİN DECORATOR (@property)
# ==========================================

class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age
    
    @property
    def age(self):
        """Age'i private yapar ve okuma/kontrol sağlar"""
        return self._age
    
    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("Yaş negatif olamaz!")
        self._age = value

# person = Person("Ahmet", 25)
# print(person.age)  # 25
# person.age = 30
# person.age = -5  # Hata: Yaş negatif olamaz!

# ==========================================
# 5. GERÇEK HAYAT ÖRNEĞİ: LOG DECORATOR
# ==========================================

def log_decorator(func):
    """Fonksiyon çağrılarını loglar"""
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__} çağrıldı")
        print(f"[LOG] Parametreler: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] Sonuç: {result}")
        return result
    return wrapper

@log_decorator
def add(a, b):
    return a + b

# result = add(5, 3)
# Çıktı:
# [LOG] add çağrıldı
# [LOG] Parametreler: args=(5, 3), kwargs={}
# [LOG] Sonuç: 8

# ==========================================
# ÖNEMLİ NOKTALAR:
# ==========================================
# - Decorator'lar fonksiyonları sarmalayan fonksiyonlardır
# - @sembolü ile kullanılır
# - *args ve **kwargs ile parametreleri geçirebilir
# - Birkaç decorator'ı birlikte kullanabilirsiniz
# - Kolay kod tekrarını önler

