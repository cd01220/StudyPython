
wordTypes = {
    "adjective": "adj.", 
    "adverb"   : "adv.", 
    "noun"     : "n.", 
    "pronoun"  : "pron.", 
    "verb"     : "v."
}

ignorePatens = ["Collocations", "Extra examples", "enlarge image", "see also", "See related", "Synonyms", "Wordfinder", "Word Origin"]

doIgnore = True
type = ""
phonetic = ""
name = ""
firstText = ""
for line in open('tmp.txt'):
    line = "".join(line.split("\n")).strip()
    if len(line.strip()) == 0:
        continue
        
    # save word name
    if name == "":
        name = line
        continue    
        
    # save word type
    if line in wordTypes:
        type = wordTypes[line]
        continue

    # save phonetic symbol
    if "NAmE" in line and phonetic == "":
        if "/" in line:
            phonetic = line[line.find("/"):len(line)]
        else:
            # phrase, no phonetic symbol
            phonetic = "//"
        continue
        
    if doIgnore == True:
        if line != "Add to my wordlist":
            continue;
        else:
            doIgnore = False
            continue;
    
    if firstText == "":
        firstText = line
        print(name, phonetic, "(word building: #)")
        if line[0:1].isdigit():
            print(type, line)
        else:
            print(type, "1", line)
        continue
        
    isIgnoredLine = False
    for i in ignorePatens:
        if i == line[0:len(i)]:
            isIgnoredLine = True
            break
            
    if isIgnoredLine:
        continue
    
    if line[0:1].isdigit():
        print(line)
    else:
        print(":", line)
    
    