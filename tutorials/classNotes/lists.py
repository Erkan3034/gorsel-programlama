def creation_and_basic():
    print("== Oluşturma ve Temel İşlemler ==")
    a = []                      # boş liste
    b = [1, 2, 3]               # sayılardan oluşan liste
    c = ["a", 1, True]          # farklı türler bir arada olabilir
    d = list(range(5))          # [0,1,2,3,4]
    e = [0] * 3                 # [0,0,0]
    print("a: ([])", a)
    print("b: ([1,2,3])", b)
    print("c: ([a,1,True])", c)
    print("d: (list(range(5)))", d)
    print("e: ([0] * 3)", e)
    print()

def indexing_and_slicing():
    print("== İndeksleme ve Dilimleme (Index & Slice) ==")
    L = ['a','b','c','d','e']
    print("L:", L)
    print("L[0]:", L[0])        # ilk eleman
    print("L[-1]:", L[-1])      # son eleman
    print("L[1:4]:", L[1:4])    # 1. dahil, 4. hariç
    print("L[:3]:", L[:3])      # baştan 3 elemana kadar
    print("L[::2]:", L[::2])    # 2'şer atlayarak
    print()

def mutability_and_methods():
    print("== Değiştirilebilirlik ve Basit Metodlar ==")
    L = [10, 20, 30]
    print("Başlangıç L:", L)
    L.append(40)                # sona ekleme
    print("append(40):", L)
    L.insert(1, 15)             # belirtilen indekse ekleme
    print("insert(1,15):", L)
    removed = L.pop()           # son elemanı alıp döndürür
    print("pop():", removed, "->", L)
    L.remove(15)                # ilk bulduğu değeri siler
    print("remove(15):", L)
    print("index(20):", L.index(20))
    print("count(20):", L.count(20))
    L.reverse()
    print("reverse():", L)
    L.sort()
    print("sort():", L)
    L.clear()
    print("clear():", L)
    print()

def list_comprehensions():
    print("== List Comprehensions (Kısa Yazım) ==")
    nums = [0,1,2,3,4,5]
    squares = [x*x for x in nums]
    even = [x for x in nums if x % 2 == 0]
    print("nums:", nums)
    print("squares:", squares)
    print("even:", even)
    print()

def simple_iteration():
    print("== Dolaşma (iteration) ve enumerate ==")
    items = ['a','b','c']
    print("Liste üzerinde normal dolaşma:")
    for v in items:
        print(v)
    print("enumerate ile (index, değer):")
    for i, v in enumerate(items):
        print(i, v)
    print()

def zip_example():
    print("== zip ile birleştirme ==")
    keys = ['name','age']
    vals = ['Alice', 30]
    d = dict(zip(keys, vals))
    print("zip -> dict:", d)
    print()

def common_operations():
    print("== Yaygın Operasyonlar ==")
    L = [3,1,4,1,5]
    print("5 in L?", 5 in L)                  # membership
    print("[1,2] + [3,4] ->", [1,2]+[3,4])    # birleştirme
    a, b, *rest = L                            # unpacking
    print("a,b,rest ->", a, b, rest)
    print("min,max,sum ->", min(L), max(L), sum(L))
    print()

def sorted_vs_sort():
    print("== sorted vs list.sort() ==")
    L = [3,1,4,1,5]
    s1 = sorted(L)     # yeni liste döner
    L.sort()           # yerinde değiştirir
    print("sorted ->", s1)
    print("after L.sort() ->", L)
    print()

def examples_summary():
    print("== Kısa Örnek Çıktısı ==")
    fruits = ["apple", "banana", "cherry"]
    a = [f.upper() for f in fruits if 'a' in f]
    print("'a' içeren meyveler (büyük harf):", a)
    for idx, val in enumerate(fruits):
        print(idx, val)
    print()

if __name__ == "__main__":
    creation_and_basic()
    indexing_and_slicing()
    mutability_and_methods()
    list_comprehensions()
    simple_iteration()
    zip_example()
    common_operations()
    sorted_vs_sort()
    examples_summary()