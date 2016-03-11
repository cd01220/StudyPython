
doIgnore = True
type = ""
phonetic = ""
name = ""
firstText = ""
for line in open('tmp.txt'):
    line = "".join(line.split("\n")).strip()
    if len(line.strip()) == 0:
        continue
    
    if name == "":
        name = line
        continue    
        
    if line.find("adjective") != -1:
        type = "adj."
        continue
    if line.find("adverb") != -1:
        type = "adv."
        continue
    if line.find("noun") != -1:
        type = "n."
        continue
    if line.find("pronoun") != -1:
        type = "pron."
        continue
    if line.find("verb") != -1:
        type = "v."
        continue

    if line.find("NAmE") != -1 and phonetic == "":
        phonetic = line[line.find("/"):len(line)]
        continue
        
    if doIgnore == True:
        if line != "Add to my wordlist":
            continue;
        else:
            doIgnore = False
            continue;
    
    if firstText == "":
        firstText = line
        print(name, phonetic)
        if line[0:1].isdigit():
            print(type, line)
        else:
            print(type, "1", line)
        continue
    
    if line[0:1].isdigit():
        print(line)
    else:
        print(":", line)
    
    