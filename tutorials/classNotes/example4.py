from collections import deque
import copy
import itertools

def creation_and_basic():
    print("== Oluşturma ve Temel İşlemler ==")
    a = []                      # boş liste
    b = [1, 2, 3]               # integer liste
    c = ["a", 1, True, None]    # heterojen liste
    d = list(range(5))          # [0,1,2,3,4]
    e = [0] * 5                 # [0,0,0,0,0]
    print("a:", a)
    print("b:", b)
    print("c:", c)
    print("d:", d)
    print("e:", e)
    print()

def indexing_and_slicing():
    print("== İndeksleme ve Dilimleme (Index & Slice) ==")
    L = ['a','b','c','d','e']
    print("L:", L)
    print("L[0]:", L[0])
    print("L[-1]:", L[-1])
    print("L[1:4]:", L[1:4])    # ['b','c','d']
    print("L[:3]:", L[:3])
    print("L[::2]:", L[::2])    # atlayarak alma
    # dilimler yeni liste üretir (shallow copy)
    s = L[1:4]
    print("s (slice):", s)
    print()

def mutability_and_methods():
    print("== Değiştirilebilirlik ve Yaygın Metodlar ==")
    L = [10, 20, 30]
    print("Başlangıç L:", L)
    L.append(40)                # sona ekleme
    print("append(40):", L)
    L.insert(1, 15)             # belirtilen indekse ekleme
    print("insert(1,15):", L)
    L.extend([50, 60])          # listeyi uzatma
    print("extend([50,60]):", L)
    removed = L.pop()           # son elemanı alıp döndürür
    print("pop():", removed, "->", L)
    removed2 = L.pop(1)         # belirli indeksi çıkar
    print("pop(1):", removed2, "->", L)
    L.remove(30)                # ilk bulduğu değeri siler
    print("remove(30):", L)
    print("index 20:", L.index(20))
    print("count of 20:", L.count(20))
    L.reverse()
    print("reverse():", L)
    L.sort()                    # yerinde sıralama (karşılaştırılabilir öğeler)
    print("sort():", L)
    L.clear()
    print("clear():", L)
    print()

def list_comprehensions():
    print("== List Comprehensions (Hızlı ve Pythonik) ==")
    nums = [0,1,2,3,4,5,6,7,8,9]
    squares = [x*x for x in nums]
    even_squares = [x*x for x in nums if x%2==0]
    nested = [(x,y) for x in range(3) for y in range(2)]
    print("nums:", nums)
    print("squares:", squares)
    print("even_squares:", even_squares)
    print("nested pairs:", nested)
    # string işleme
    words = ["  apple ", "Banana", "Cherry  "]
    cleaned = [w.strip().lower() for w in words]
    print("cleaned:", cleaned)
    print()

def nested_lists_and_flattening():
    print("== İç İçe Listeler ve Düzleştirme (Nested) ==")
    mat = [[1,2,3],[4,5,6],[7,8,9]]
    print("mat:", mat)
    # 1 seviye düzleştirme
    flat = [x for row in mat for x in row]
    print("flat:", flat)
    # derin düzleştirme (itertools.chain)
    flat2 = list(itertools.chain.from_iterable(mat))
    print("flat2 (chain):", flat2)
    print()

def list_as_stack_and_queue():
    print("== Stack ve Queue Örnekleri ==")
    stack = []                 # LIFO: append/pop
    stack.append(1); stack.append(2); stack.append(3)
    print("stack before:", stack)
    print("stack pop:", stack.pop())
    print("stack after:", stack)

    # Queue için deque kullanın (popleft O(1))
    q = deque()
    q.append(1); q.append(2); q.append(3)
    print("queue before:", q)
    print("queue popleft:", q.popleft())
    print("queue after:", q)
    print()

def iteration_enumerate_zip():
    print("== Dolaşma (iteration), enumerate, zip ==")
    items = ['a','b','c']
    for i, v in enumerate(items):
        print(f"index {i} value {v}")
    keys = ['name','age']
    vals = ['Alice', 30]
    d = dict(zip(keys, vals))
    print("zip -> dict:", d)
    print()

def copying_shallow_deep():
    print("== Kopyalama: Shallow vs Deep ==")
    orig = [[1,2], [3,4]]
    shallow = list(orig)           # ya da orig.copy()
    deep = copy.deepcopy(orig)
    orig[0].append(99)
    print("orig:", orig)
    print("shallow (paylaşımlı iç nesneler):", shallow)  # iç listeler paylaşılır
    print("deep (bağımsız):", deep)
    print()

def common_operations_and_tricks():
    print("== Yaygın Operasyonlar ve Püf Noktaları ==")
    L = [3,1,4,1,5,9,2]
    # membership
    print("5 in L?", 5 in L)
    # concatenation and repetition
    print("[1,2] + [3,4] ->", [1,2]+[3,4])
    print("[0]*3 ->", [0]*3)
    # unpacking
    a, b, *rest = L
    print("a,b,rest ->", a,b,rest)
    # min, max, sum
    print("min,max,sum ->", min(L), max(L), sum(L))
    # sorted vs list.sort()
    s1 = sorted(L)   # yeni liste döner
    L.sort()         # yerinde değiştirir
    print("sorted ->", s1, "after L.sort() ->", L)
    print()

def functional_tools_and_generators():
    print("== map/filter/reduce ve generator expressions ==")
    nums = list(range(10))
    doubled = list(map(lambda x: x*2, nums))
    evens = list(filter(lambda x: x%2==0, nums))
    # generator expression (hafıza dostu)
    gen = (x*x for x in nums)
    print("doubled:", doubled)
    print("evens:", evens)
    print("gen next:", next(gen), next(gen))  # örnek tüketim
    print()

def pitfalls_and_performance_notes():
    print("== Tuzaklar ve Performans Notları ==")
    # 1) aynı liste referansından oluşan tekrar:
    rows = [[0]*3]*3   # dikkat: iç listeler aynı referansı paylaşır
    rows[0][0] = 9
    print("rows (yanlış kullanım):", rows)
    # doğru yol:
    rows2 = [[0]*3 for _ in range(3)]
    rows2[0][0] = 9
    print("rows2 (doğru):", rows2)

    # 2) büyük veride generator comprehension bellek tasarrufu sağlar
    big = (i for i in range(10**6))
    print("big generator hazır (tüketim yok)")

    # 3) list concatenation in loop (O(n^2) olabilir) - kullanmayın:
    s = []
    for i in range(1000):
        s += [i]   # yavaş; append kullanın
    # doğru:
    s2 = []
    for i in range(1000):
        s2.append(i)
    print("constructed lists lengths:", len(s), len(s2))
    print()

def examples_summary():
    print("== Kısa Örnek Çıktısı ==")
    # küçük bir örnek birleştiriyoruz:
    fruits = ["apple", "banana", "cherry"]
    # comprehension + filter
    a = [f.upper() for f in fruits if 'a' in f]
    print("fruits with 'a' uppercased:", a)
    # enumerate kullanımı
    for idx, val in enumerate(fruits):
        print(idx, val)
    print()

if __name__ == "__main__":
    creation_and_basic()
    indexing_and_slicing()
    mutability_and_methods()
    list_comprehensions()
    nested_lists_and_flattening()
    list_as_stack_and_queue()
    iteration_enumerate_zip()
    copying_shallow_deep()
    common_operations_and_tricks()
    functional_tools_and_generators()
    pitfalls_and_performance_notes()
    examples_summary()