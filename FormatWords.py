from html.parser import HTMLParser
from html.entities import name2codepoint
import codecs
import io
import sys  
 
class MyHtmlParser(HTMLParser):        
    def __init__(self):
        HTMLParser.__init__(self, strict=False)      
        self.StartTagHandler = \
        {
            ("div", ("class", "webtop-g")):     self.HandleStartTagDivClassWebtopg,
            ("span", ("class", "phon")):        self.HandleStartTagSpanClassPhon, 
            ("span", ("class", "sn-g")):        self.HandleStartTagSpanClassSng,
            ("li", ("class", "sn-g")):          self.HandleStartTagLiClassSng,            
            ("span", ("class", "x-g")):         self.HandleStartTagSpanClassXg,
            ("span", ("class", "gram-g")):      self.HandleStartTagSpanClassGramg,
            ("span", ("class", "use")):         self.HandleStartTagSpanClassUse,
            ("span", ("class", "collapse")):    self.HandleStartTagSpanClassCollapse,
            ("span", ("class", "idm-gs")):      self.HandleStartTagSpanClassIdmgs,
            ("a",    ("class", "Ref")):         self.HandleStartTagAClassRef,
            ("span", ("class", "v-gs")):        self.HandleStartTagAClassVgs,
            ("span", ("class", "label-g")):     self.HandleStartTagAClassLabelg,
            ("span", ("class", "un")):          self.HandleStartTagSpanClassUn
        }
        self.EndTagHandler = \
        {
            ("div", ("class", "webtop-g")):     self.HandleEndTagDivClassWebtopg,    
            ("span", ("class", "phon")):        self.HandleEndTagSpanClassPhon,     
            ("span", ("class", "sn-g")):        self.HandleEndTagSpanClassSng,
            ("li", ("class", "sn-g")):          self.HandleEndTagLiClassSng,
            ("span", ("class", "x-g")):         self.HandleEndTagSpanClassXg,
            ("span", ("class", "gram-g")):      self.HandleEndTagSpanClassGramg,
            ("span", ("class", "use")):         self.HandleEndTagSpanClassUse,
            ("span", ("class", "collapse")):    self.HandleEndTagSpanClassCollapse,
            ("span", ("class", "idm-gs")):      self.HandleEndTagSpanClassIdmgs,
            ("a",    ("class", "Ref")):         self.HandleEndTagAClassRef,
            ("span", ("class", "v-gs")):        self.HandleEndTagAClassVgs,
            ("span", ("class", "label-g")):     self.HandleEndTagAClassLabelg,
            ("span", ("class", "un")):          self.HandleEndTagSpanClassUn
        }
        self.DataHandler = \
        {        
            ("h2", ("class", "h")):             self.HandleDataTagH2ClassH, 
            ("span", ("class", "phon")):        self.HandleDataTagSpanClassPhon, 
            ("span", ("class", "wrap")):        self.HandleDataTagSpanClassWrap,
            ("span", ("class", "sep")):         self.HandleDataTagSpanClassSep,
            ("span", ("class", "cl")):          self.HandleDataTagSpanClassCl,
            ("span", ("class", "ptl")):         self.HandleDataTagSpanClassPtl,
            ("strong", ("class", "pseudo")):    self.HandleDataTagStrongClassPseudo,
            ("span", ("class", "pos")):         self.HandleDataTagSpanClassPos,           
            ("span", ("class", "def")):         self.HandleDataTagSpanClassDef,
            ("span", ("class", "x")):           self.HandleDataTagSpanClassX,
            ("span", ("class", "cf")):          self.HandleDataTagSpanClassCf, 
            ("span", ("class", "exp")):         self.HandleDataTagSpanClassExp,           
            ("span", ("class", "gram")):        self.HandleDataTagSpanClassGram,            
            ("span", ("class", "use")):         self.HandleDataTagSpanClassUse, 
            ("span", ("class", "name")):        self.HandleDataTagSpanClassName,
            ("span", ("class", "prefix")):      self.HandleDataTagSpanClassPrefix,
            ("span", ("class", "gl")):          self.HandleDataTagSpanClassGl,
            ("span", ("class", "ndv")):         self.HandleDataTagSpanClassNdv,
            ("span", ("class", "reg")):         self.HandleDataTagSpanClassReg,
            ("span", ("class", "dtxt")):         self.HandleDataTagSpanClassDtxt,
            ("span", ("class", "xh")):          self.HandleDataTagSpanClassXh,
            ("span", ("class", "xs")):          self.HandleDataTagSpanClassXs 
        }
        #const
        self.IgnoreCategoris = ["collapse", "idm-gs", "A-Ref", "v-gs", "un"]
        #member variable 1
        self.tagAttrs = []   #[("span", ("class", "def")]
        #member variable 2
        self.wordName = ""
        self.wordPhon = ""
        self.wordPhonType = ""
        self.wordClass = ""
        self.dataCategoris = ["bottom"]  #add the "bottom" to make sure the list never be empty
        self.definitionTuples = []
        self.definitionTuple = {"definition": {"def": "", "cfexp": "", "exp": "", "gram": "", "pos": "", "use": ""}, "examples": []}
        self.example = {"x": "", "cfexp": ""}
        self.areaFlag = "definition"
       
    #######################start tag handler
    def HandleStartTagDivClassWebtopg(self):
        if self.dataCategoris[len(self.dataCategoris) - 1] in self.IgnoreCategoris:
            return
        self.dataCategoris.append("webtop-g")
    
    def HandleStartTagSpanClassPhon(self):
        if self.dataCategoris[len(self.dataCategoris) - 1] in self.IgnoreCategoris:
            return
        self.dataCategoris.append("phon")
        
    def HandleStartTagSpanClassSng(self):
        if self.dataCategoris[len(self.dataCategoris) - 1] in self.IgnoreCategoris:
            return
        self.dataCategoris.append("sn-g")
        self.areaFlag = "definition"
        
    def HandleStartTagLiClassSng(self):  
        self.HandleStartTagSpanClassSng()
                
    def HandleStartTagSpanClassXg(self):
        if self.dataCategoris[len(self.dataCategoris) - 1] in self.IgnoreCategoris:
            return
        self.dataCategoris.append("x-g")
        self.areaFlag = "example"
        
    def HandleStartTagSpanClassGramg(self):
        if self.dataCategoris[len(self.dataCategoris) - 1] in self.IgnoreCategoris:
            return
        self.dataCategoris.append("gram-g")
        
    def HandleStartTagSpanClassUse(self):
        if self.dataCategoris[len(self.dataCategoris) - 1] in self.IgnoreCategoris:
            return
        self.dataCategoris.append("use")
        
    def HandleStartTagSpanClassCollapse(self):
        self.dataCategoris.append("collapse")
        
    def HandleStartTagSpanClassIdmgs(self):
        self.dataCategoris.append("idm-gs")
    
    def HandleStartTagAClassRef(self):
        self.dataCategoris.append("A-Ref")
    
    def HandleStartTagAClassVgs(self):
        self.dataCategoris.append("v-gs")
        
    def HandleStartTagAClassLabelg(self):
        self.dataCategoris.append("label-g")
    
    def HandleStartTagSpanClassUn(self):
        self.dataCategoris.append("un")
        
    #######################end tag handler
    def HandleEndTagDivClassWebtopg(self):
        size = len(self.dataCategoris)
        if self.dataCategoris[len(self.dataCategoris) - 1] in self.IgnoreCategoris:
            return
        assert self.dataCategoris[len(self.dataCategoris) - 1] == "webtop-g"
        self.dataCategoris.pop()
    
    def HandleEndTagSpanClassPhon(self):
        size = len(self.dataCategoris)
        if self.dataCategoris[len(self.dataCategoris) - 1] in self.IgnoreCategoris:
            return
        assert self.dataCategoris[len(self.dataCategoris) - 1] == "phon"
        self.wordPhonType = ""
        self.dataCategoris.pop()        
    
    def HandleEndTagSpanClassSng(self):
        size = len(self.dataCategoris)
        if self.dataCategoris[len(self.dataCategoris) - 1] in self.IgnoreCategoris:
            return
        assert self.dataCategoris[len(self.dataCategoris) - 1] == "sn-g"
        self.dataCategoris.pop()
        self.AddDefinitionTupleIntoDefinitionTuples()
        self.definitionTuple = \
        {
            "definition": {"cfexp": "", "def": "", "gram": "", "pos": "", "use": ""}, 
            "examples": []
        }
        
    def HandleEndTagLiClassSng(self):  
        self.HandleEndTagSpanClassSng() 
        
    def HandleEndTagSpanClassXg(self):
        size = len(self.dataCategoris)
        if self.dataCategoris[size - 1] in self.IgnoreCategoris:
            return        
        assert self.dataCategoris[size - 1] == "x-g"
        self.dataCategoris.pop()
        self.AddExampleIntoDefinitionTuple()
        self.example = {"x": "", "cfexp": ""}
        
    def HandleEndTagSpanClassGramg(self):
        size = len(self.dataCategoris)
        if self.dataCategoris[size - 1] in self.IgnoreCategoris:
            return
        assert self.dataCategoris[size - 1] == "gram-g"
        self.dataCategoris.pop()       
        
    def HandleEndTagSpanClassUse(self):
        size = len(self.dataCategoris) 
        if self.dataCategoris[size - 1] in self.IgnoreCategoris:
            return
        assert self.dataCategoris[size - 1] == "use"
        self.dataCategoris.pop()
        
    def HandleEndTagSpanClassCollapse(self):
        assert self.dataCategoris[len(self.dataCategoris) - 1] == "collapse"
        self.dataCategoris.pop()
        
    def HandleEndTagSpanClassIdmgs(self):
        assert self.dataCategoris[len(self.dataCategoris) - 1] == "idm-gs"
        self.dataCategoris.pop()
        
    def HandleEndTagAClassRef(self):
        assert self.dataCategoris[len(self.dataCategoris) - 1] == "A-Ref"
        self.dataCategoris.pop()
        
    def HandleEndTagAClassVgs(self):
        assert self.dataCategoris[len(self.dataCategoris) - 1] == "v-gs"
        self.dataCategoris.pop()
        
    def HandleEndTagAClassLabelg(self):
        assert self.dataCategoris[len(self.dataCategoris) - 1] == "label-g"
        self.dataCategoris.pop()
        
    def HandleEndTagSpanClassUn(self):
        assert self.dataCategoris[len(self.dataCategoris) - 1] == "un"
        self.dataCategoris.pop()
        
    #######################data handler       
    def HandleDataTagH2ClassH(self, data):
        size = len(self.dataCategoris)
        if self.dataCategoris[size - 1] in self.IgnoreCategoris:
            return            
        assert self.dataCategoris[len(self.dataCategoris) - 1] == "webtop-g"
        self.wordName = data
    
    def HandleDataTagSpanClassPhon(self, data):
        size = len(self.dataCategoris)
        if self.dataCategoris[size - 1] in self.IgnoreCategoris:
            return
        assert self.dataCategoris[len(self.dataCategoris) - 1] == "phon"
        if self.wordPhonType == "NAmE":
            self.wordPhon += data
    
    def HandleDataTagSpanClassWrap(self, data):
        size = len(self.dataCategoris)
        if self.dataCategoris[size - 1] in self.IgnoreCategoris:
            return            
        category = self.dataCategoris[len(self.dataCategoris) - 1]
        if category == "sn-g" or category == "x-g":
            if self.areaFlag == "definition":
                self.definitionTuple["definition"]["def"] += data
            elif category == "x-g":
                self.example["x"] += data
        elif category == "gram-g":
            self.definitionTuple["definition"]["gram"] += data
        elif category == "use":
            self.definitionTuple["definition"]["use"] += data
        elif category == "phon" and self.wordPhonType == "NAmE":
            self.wordPhon += data
    
    def HandleDataTagSpanClassSep(self, data):
        self.HandleDataTagSpanClassWrap(data)
        
    def HandleDataTagSpanClassCl(self, data):
        self.HandleDataTagSpanClassWrap(data)
        
    def HandleDataTagSpanClassPtl(self, data):
        self.HandleDataTagSpanClassWrap(data)
    
    def HandleDataTagStrongClassPseudo(self, data):
        self.HandleDataTagSpanClassWrap(data)
       
    def HandleDataTagSpanClassPrefix(self, data):
        size = len(self.dataCategoris)
        if self.dataCategoris[size - 1] in self.IgnoreCategoris:
            return            
        category = self.dataCategoris[len(self.dataCategoris) - 1]
        if category == "x-g" and self.areaFlag == "example":
            self.example["x"] += data
        
    def HandleDataTagSpanClassGl(self, data):
        self.HandleDataTagSpanClassWrap(data)
        
    def HandleDataTagSpanClassNdv(self, data):
        self.HandleDataTagSpanClassWrap(data)
        
    def HandleDataTagSpanClassReg(self, data):
        self.HandleDataTagSpanClassWrap(data)
        
    def HandleDataTagSpanClassDtxt(self, data):
        self.HandleDataTagSpanClassWrap(data)
        
    def HandleDataTagSpanClassXh(self, data):
        self.HandleDataTagSpanClassWrap(data)
        
    def HandleDataTagSpanClassXs(self, data):
        self.HandleDataTagSpanClassWrap(data)
        
    def HandleDataTagSpanClassPos(self, data):  
        size = len(self.dataCategoris)
        if self.dataCategoris[size - 1] in self.IgnoreCategoris:
            return            
        category = self.dataCategoris[len(self.dataCategoris) - 1]
        if category == "sn-g":
            self.definitionTuple["definition"]["pos"] += data
        elif category == "webtop-g":
            self.wordClass = data

    def HandleDataTagSpanClassDef(self, data): 
        size = len(self.dataCategoris)
        if self.dataCategoris[size - 1] in self.IgnoreCategoris:
            return            
        assert self.dataCategoris[len(self.dataCategoris) - 1] == "sn-g"
        self.definitionTuple["definition"]["def"] += data
    
    def HandleDataTagSpanClassX(self, data):  
        size = len(self.dataCategoris)
        if self.dataCategoris[size - 1] in self.IgnoreCategoris:
            return            
        assert self.dataCategoris[len(self.dataCategoris) - 1] == "x-g"
        self.example["x"] += data
     
    def HandleDataTagSpanClassCf(self, data): 
        size = len(self.dataCategoris)
        if self.dataCategoris[size - 1] in self.IgnoreCategoris:
            return            
        category = self.dataCategoris[len(self.dataCategoris) - 1]    
        if category == "sn-g" or category == "x-g":
            if self.areaFlag == "definition":
                self.definitionTuple["definition"]["cfexp"] += data
            else:
                self.example["cfexp"] += data
        else:
            pass  #ignore "cf", "exp" not surrounded by "sn-g" or "x-g"
    
    def HandleDataTagSpanClassExp(self, data):
        self.HandleDataTagSpanClassCf(data)
        
    def HandleDataTagSpanClassGram(self, data):
        size = len(self.dataCategoris)
        if self.dataCategoris[size - 1] in self.IgnoreCategoris:
            return            
        assert self.dataCategoris[len(self.dataCategoris) - 1] == "gram-g"
        self.definitionTuple["definition"]["gram"] += data
            
    def HandleDataTagSpanClassUse(self, data):
        size = len(self.dataCategoris)
        if self.dataCategoris[size - 1] in self.IgnoreCategoris:
            return            
        assert self.dataCategoris[len(self.dataCategoris) - 1] == "use"
        self.definitionTuple["definition"]["use"] += data
    
    def HandleDataTagSpanClassName(self, data):
        size = len(self.dataCategoris)
        if self.dataCategoris[size - 1] in self.IgnoreCategoris:
            return            
        assert self.dataCategoris[len(self.dataCategoris) - 1] == "phon"
        self.wordPhonType = data
        
    #######################overwrited function    
    #tag:   "span"
    #attrs: (("class", "def"), ("id", "look_1__72"), ...)
    def handle_starttag(self, tag, attrs):
        if len(attrs) != 0 and len(attrs[0]) != 0:
            tagAttr = (tag, attrs[0]) 
        else:
            #pseudo tuple to invoid unnecessary comparation  
            tagAttr = (tag, ("class", "pseudo"))  
        if tagAttr in self.StartTagHandler:
            self.StartTagHandler[tagAttr]()        
        self.tagAttrs.append(tagAttr)
            
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
    
    #######################private function
    def AddDefinitionTupleIntoDefinitionTuples(self):
        string = "[] "
        if self.definitionTuple["definition"]["gram"] != "":
            string = self.definitionTuple["definition"]["gram"] + " "
        if self.definitionTuple["definition"]["pos"] != "":
            string = string + self.definitionTuple["definition"]["pos"] + " "
        if self.definitionTuple["definition"]["use"] != "":
            string = string + self.definitionTuple["definition"]["use"] + " "
        if self.definitionTuple["definition"]["cfexp"] != "":
            string = string + self.definitionTuple["definition"]["cfexp"] + " "
        string = string + self.definitionTuple["definition"]["def"]
        if string == "[] ":
            return
        self.definitionTuples.append({"definition": string, "examples": self.definitionTuple["examples"]})

    def AddExampleIntoDefinitionTuple(self):
        if self.example["cfexp"] == "":
            self.definitionTuple["examples"].append(self.example["x"])
        else:
            self.definitionTuple["examples"].append(self.example["cfexp"] + " " + self.example["x"])
    
    #######################public function    
    def ReadResult(self):
        output = [self.wordName + self.wordPhon + "(word building: #)"]
        index = 1
        for i in self.definitionTuples:
            if index == 1:
                output.append(self.wordClass + ". " + str(index) + " " + i["definition"])
            else:
                output.append(str(index) + " " + i["definition"])
            for ii in i["examples"]:
                output.append(": " + ii)
            index = index + 1
        return output

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-16')                 
    parser = MyHtmlParser()
    assert len(sys.argv) == 2
    srcFileObj = codecs.open(sys.argv[1], "r", "utf-8")

    for line in srcFileObj:
        parser.feed(line)
    
    for i in parser.ReadResult():
        print(i)