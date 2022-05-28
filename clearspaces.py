file = open("data/gisaid.fasta", "r")
data = file.read()
file.close()
file = open("data/tweaked.fasta", "w")
charArray = []
for char in data:
    if char != ' ':
        charArray.append(char)
str = ""
for char in charArray:
    str += char
file.write(str)
file.close()
