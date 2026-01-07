with open ("primes_safe.txt", "r") as file:
    content = file.read()

    print(content)


with open ("write_file.txt", "w", encoding = "utf-8") as write_file:
    write_file.write("Merhaba Dünya!\n")
    write_file.write("Python ile dosya işlemleri.\n")



with open ("append_file.txt" , "a" , encoding="utf-8") as append_file:
    append_file.write("Bu satır append ile eklendi.\n")

