a = 5
b = 0

b = int(input('Unesi broj: '))

if b==2:
    a=10
elif b==5:
    a = 5
    a = c

print(a)

"""
ovo je blok komentar
i ovo
"""
d = 2.32323232

print("d je {:.2f}".format(d))

s = "ovo je prvi string"
print(s[1])
# s[1] = 'd'

s2 = input('Unesi string: ')


while input('unesi slovo:') != 'k':
    print("while nesto")
    if (input('unesi slovo:')) == 'a':
        break
    else:
        continue
else:
    "kraj while"

print(s[::-1])
for x in s:
    print(x)