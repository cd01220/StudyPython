from html.parser import HTMLParser
from html.entities import name2codepoint
import codecs
import io
import sys  
 
class MyHtmlParser(HTMLParser):        
    def __init__(self):
        HTMLParser.__init__(self, strict=False)
        self.tagAttrs = []   #[("span", ("class", "def")]
        self.defs = []   #[("definition", (example sentence 1, example sentence 2, ...))]
        self.EndTagHandler = \
        {
            ("span", ("class", "def")): self.HandleEndTagSpanClassDef, 
            ("span", ("class", "x-g")): self.HandleEndTagSpanClassXg
        }
        self.DataHandler = \
        {
            ("h2", ("class", "h")): self.HandleDataTagH2ClassH, 
            ("span", ("class", "phon")): self.HandleDataTagSpanClassPhon, 
            ("span", ("class", "pos")): self.HandleDataTagSpanClassPos,
            ("span", ("class", "cf")): self.HandleDataTagSpanClassCf, 
            ("span", ("class", "exp")): self.HandleDataTagSpanClassExp,
            ("span", ("class", "use")): self.HandleDataTagSpanClassUse,            
            ("span", ("class", "def")): self.HandleDataTagSpanClassDef,
            ("span", ("class", "eb")): self.HandleDataTagSpanClassEb,
            ("span", ("class", "ndv")): self.HandleDataTagSpanClassNdv,            
            ("span", ("class", "gram")): self.HandleDataTagSpanClassGram,
            ("span", ("class", "x")): self.HandleDataTagSpanClassX,
            ("span", ("class", "gl")): self.HandleDataTagSpanClassGl,
            ("strong", ("class", "pseudo")): self.HandleDataTagStrongClassPseudo
        }
        #temp data
        self.tmpName = ""
        self.tmpPhon = "" 
        self.tmpPos = ""   #verb, noun, ...
        self.tmpGram = ""  #transitive, intransitive, ...
        self.tmpUse = ""   #(not usually used in the progressive tenses)
        self.tmpDef = ""
        self.tmpExampleSentence = ""
    
    def CheckStack(self, subStack):
        totalStack = self.tagAttrs
        assert len(totalStack) > 0 and len(subStack) > 0
        m = len(totalStack)
        for subTop in subStack[::-1]:
            for m in range(m, 0, -1):
                if subTop == totalStack[m-1]:
                    break
            m = m - 1
            if subTop != totalStack[m]:
                return False
        excludeTag = [("span", ("class", "collapse")), ("span", ("class", "idm-gs"))]
        for i in totalStack:
            for ii in excludeTag:
                if i == ii:
                    return False                
        return True         
     
    #return: "definition" or "example sentence" or "" 
    def GetDataType(self):
        dataType = ("pseudo", ("class", "pseudo"))
        i = len(self.tagAttrs)
        for i in range(len(self.tagAttrs), 0, -1):
            tagAttr = self.tagAttrs[i-1]
            if tagAttr[0] == "span":
                if tagAttr[1][0] == "class":
                    if tagAttr[1][1] in ["sn-gs", "x-gs"]:
                        dataType = tagAttr
                        break
        return dataType
     
    #######################end tag handler
    def HandleEndTagSpanClassDef(self):
        if self.CheckStack([("ol", ("class", "h-g")), 
                            ("span",("class", "sn-gs")),
                            ("li",("class", "sn-g"))]):
            if self.tmpUse == "":
                self.defs.append(("[" + self.tmpGram + "] " + self.tmpDef, []))
            else:
                self.defs.append(("[" + self.tmpGram + "] (" + self.tmpUse + ") " + self.tmpDef, []))
        self.tmpGram = ""
        self.tmpUse = ""
        self.tmpDef = ""
        
    def HandleEndTagSpanClassXg(self):
        if self.CheckStack([("ol", ("class", "h-g")), 
                            ("span",("class", "sn-gs")),
                            ("li",("class", "sn-g")),
                            ("span",("class", "x-gs"))]):
            curDef = self.defs.pop()
            curDef[1].append(self.tmpExampleSentence)
            self.defs.append(curDef)
        self.tmpExampleSentence = ""
        
    #######################data handler        
    def HandleDataTagH2ClassH(self, data):
        self.tmpName = data
        
    def HandleDataTagSpanClassPhon(self, data):
        if self.CheckStack([("div", ("class", "top-g"))]):
            self.tmpPhon = data
        
    def HandleDataTagSpanClassPos(self, data):        
        if self.CheckStack([("div", ("class", "top-g")), ("div", ("class", "webtop-g"))]):
            self.tmpPos = data
        elif self.CheckStack([("ol", ("class", "h-g")), ("span", ("class", "gram-g"))]):
            self.tmpGram = data
        elif self.CheckStack([("ol", ("class", "h-g")),  
                              ("span", ("class", "sn-gs")),  
                              ("li", ("class", "sn-g")), 
                              ("span", ("class", "pos-g"))]):
            self.tmpGram = data
        
    def HandleDataTagSpanClassCf(self, data):
        dataType = self.GetDataType()
        if dataType == ("span", ("class", "sn-gs")):
            self.tmpDef = self.tmpDef + data + " "
        elif dataType == ("span", ("class", "x-gs")):
            self.tmpExampleSentence = self.tmpExampleSentence + data + " "
                
    def HandleDataTagSpanClassExp(self, data):
        dataType = self.GetDataType()
        if dataType == ("span", ("class", "sn-gs")):
            self.tmpDef = self.tmpDef + data
        elif dataType == ("span", ("class", "x-gs")):
            self.tmpExampleSentence = self.tmpExampleSentence + data
    
    def HandleDataTagSpanClassUse(self, data):
        self.tmpUse = self.tmpUse + data
    
    def HandleDataTagSpanClassDef(self, data):      
        self.tmpDef = self.tmpDef + data
    
    def HandleDataTagSpanClassEb(self, data):  
        if self.CheckStack([("ol", ("class", "h-g"))]):
            dataType = self.GetDataType()
            if dataType == ("span", ("class", "sn-gs")):
                self.tmpDef = self.tmpDef + data
            elif dataType == ("span", ("class", "x-gs")):
                self.tmpExampleSentence = self.tmpExampleSentence + data
    
    def HandleDataTagSpanClassNdv(self, data): 
        if self.CheckStack([("ol", ("class", "h-g"))]):
            dataType = self.GetDataType()
            if dataType == ("span", ("class", "sn-gs")):
                self.tmpDef = self.tmpDef + data
            elif dataType == ("span", ("class", "x-gs")):
                self.tmpExampleSentence = self.tmpExampleSentence + data
    
    
    def HandleDataTagSpanClassGram(self, data):
        if self.tmpGram == "":
            self.tmpGram = data
        else:
            self.tmpGram = self.tmpGram + "," + data
        
    def HandleDataTagSpanClassX(self, data):  
        self.tmpExampleSentence = self.tmpExampleSentence + data
        
    def HandleDataTagSpanClassGl(self, data): 
        if self.CheckStack([("span", ("class", "x-g")), ("span", ("class", "rx-g")), ("span", ("class", "x"))]):
            self.tmpExampleSentence = self.tmpExampleSentence + "(=" + data + ")"
        
    def HandleDataTagStrongClassPseudo(self, data):
        if self.CheckStack([("ol", ("class", "h-g"))]):
            dataType = self.GetDataType()
            if dataType == ("span", ("class", "sn-gs")):
                self.tmpDef = self.tmpDef + data
            elif dataType == ("span", ("class", "x-gs")):
                self.tmpExampleSentence = self.tmpExampleSentence + data
    
    #tag:   "span"
    #attrs: (("class", "def"), ("id", "look_1__72"), ...)
    def handle_starttag(self, tag, attrs):
        if len(attrs) != 0 and len(attrs[0]) != 0:
            self.tagAttrs.append((tag, attrs[0]))
        else:
            self.tagAttrs.append((tag, ("class", "pseudo"))) #pseudo tuple to invoid unnecessary comparation
            
    def handle_endtag(self, tag):    
        tagAttr = self.tagAttrs.pop()
        if tagAttr in self.EndTagHandler:
            self.EndTagHandler[tagAttr]()
                
    def handle_data(self, data):          
        if len(self.tagAttrs) == 0:
            return
        tagAttr = self.tagAttrs[len(self.tagAttrs) - 1]
        if tagAttr in self.DataHandler:
            self.DataHandler[tagAttr](data)
        
    def Print(self):
        print(self.tmpName, "/" + self.tmpPhon + "/", "(word building: #)")
        index = 1
        for i in self.defs:
            if index == 1:
                print(self.tmpPos + ".", end=" ")
            print(index, i[0])
            for ii in i[1]:
                print(":", ii)
            index = index + 1
    
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-16')                 
parser = MyHtmlParser()
assert len(sys.argv) == 2
srcFileObj = codecs.open(sys.argv[1], "r", "utf-8")

for line in srcFileObj:
    parser.feed(line)
    
parser.Print()