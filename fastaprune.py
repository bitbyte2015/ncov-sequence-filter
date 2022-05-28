file = open("data/tweaked.fasta", "r")
data = file.read()
file.close()
file = open("data/pruned.fasta", "w")
index = open("recombinants.csv", "r")
entries = index.read()
index.close()
entry = ""
listing = ""
for char in entries:
    if char != ',':
        entry += char
    else:
        location = data.find(entry)
        if location > -1:
            listing += data[location-1]
            char = data[location]
            while char != '>':
                listing += char
                if location < len(data)-1:
                    location += 1
                    char = data[location]
                else:
                    break
        entry = ""
file.write(listing)
file.close()
