from html.parser import HTMLParser
from html.entities import name2codepoint
import codecs
import io
import sys  
 

class MyHtmlParser(HTMLParser):        
    ''' 
    def __init__(self, effecitvePatterns, ignoredPatterns):
    input:
        effecitvePatterns = [{"pattern name": "xxx", "pattern": [("tag name", [("class", "pos")])]}]
        ignoredPatterns   = [[("span", [("class", "collapse")])], [("span", [("class", "idm-gs")])]]

    result:
    self.effecitvePatterns  = 
    {
        "name": 
        {
            value: "",
            pattern:
            [
                {
                    "tags": ("div", [("class", "webtop-g")]), 
                    "is in": False
                } 
                {
                    "tags": ("h2", [("class", "h")]), 
                    "is in": False
                }
            ]
        },
        "word class":
        {
            value: "",
            pattern:
            [
                {
                    "tags": ("div", [("class", "webtop-g")]), 
                    "is in": False
                } 
                {
                    "tags": ("span", [("class", "pos")]), 
                    "is in": False
                }
            ]
        },
        "phonetic symbol":
        {
            value: "",
            pattern:
            [
                {
                    "tags": ("div", [("class", "pron-gs ei-g")]), 
                    "is in": False
                }
                {
                    "tags": ("span", [("class", "pron-g"), ("geo", n_am)] ), 
                    "is in": False
                }
            ]
        },
        "definition":
        {
            value: "",
            pattern:
            [
                {
                    "tags": ("span|li", [("class", "sn-g")]), 
                    "is in": False
                }
            ]
        }
    }
    self.ignoredPatterns  = 
    [
        [
            {
                "tags"  : ("span", [("class", "collapse")]), 
                "is in": False
            }
        ],
        [
            {
                "tags"  : ("span", [("class", "idm-gs")]), 
                "is in": False
            }
        ],
        [
            {
                "tags"  : ("div", [("class", "sound audio_play_button pron-us icon-audio")]),
                "is in": False
            }
        ]
    ]
    ''' 
    def __init__(self, effecitvePatterns, ignoredPatterns, cssBlockTags):
        HTMLParser.__init__(self, strict=False)   
        self.tagStack = []
        self.cssBlockTags = cssBlockTags
        self.number = 1
        #if self.history == "", means there is no data between 2 block tag, do not need insert redundant 
        #line break. for example: the "blazon" has no text for its 2nd definition
        self.history = ""  
        
        self.effecitvePatterns = {}        
        for pattern in effecitvePatterns:
            name = pattern["pattern name"]
            self.effecitvePatterns[name] = {}
            self.effecitvePatterns[name]["value"] = ""
            self.effecitvePatterns[name]["pattern"] = []
            for tag in pattern["pattern"]:
                self.effecitvePatterns[name]["pattern"].append({"tags": tag, "is in": False})
                
        self.ignoredPatterns = []
        for pattern in ignoredPatterns:
            tmp = []
            for tag in pattern:
                tmp.append({"tags": tag, "is in": False})
            self.ignoredPatterns.append(tmp)
          
          
    #######################overwrited function    
    #input:
    #   tag  :   "span"
    #   attrs: (("class", "def"), ("id", "look_1__72"), ...)
    #output:
    '''
    self.tagStack = \
    [
        {
            "tag"    : ('span1', [('class', 'xxx1')]), 
            "pattern": [('effecitvePatterns', "name", 0), ('effecitvePatterns', "phon", 0)]
        },
        {
            "tag"    : ('span1', [('class', 'xxx2')]), 
            "pattern": [('effecitvePatterns', "phon", 1), ('ignoredPatterns', 0, 0)]
        },
    ]
    '''
    def handle_starttag(self, tag, attrs):
        stackProperties = []
        for i1 in self.effecitvePatterns:
            pattern = self.effecitvePatterns[i1]["pattern"]
            for i2 in range(0, len(pattern)):
                if pattern[i2]["is in"]:
                    continue              
                if self.CompareTag(pattern[i2]["tags"], (tag, attrs)):
                    pattern[i2]["is in"] = True 
                    stackProperties.append(("effecitvePatterns", i1, i2))
                break
        for i1 in range(0, len(self.ignoredPatterns)):
            pattern = self.ignoredPatterns[i1]
            for i2 in range(0, len(pattern)):
                if pattern[i2]["is in"]:
                    continue            
                if self.CompareTag(pattern[i2]["tags"], (tag, attrs)):
                    pattern[i2]["is in"] = True 
                    stackProperties.append(("ignoredPatterns", i1, i2))
                break
        
        self.tagStack.append({"tag":(tag, attrs), "pattern": stackProperties})
        #process css format
        if self.IsInPattern("definition"):    
            csStr = self.GetCssString((tag, attrs))
            if self.history != "":
                self.effecitvePatterns["definition"]["value"] += csStr
            if self.CompareTag(("span|li", [("class", "sn-g")]), (tag, attrs)):
                self.effecitvePatterns["definition"]["value"] += str(self.number) + " "
                self.number = self.number + 1
            if self.CompareTag(("span", [("class", "x-g")]), (tag, attrs)):
                self.effecitvePatterns["definition"]["value"] += ":"
            if self.CompareTag(("span", [("class", "xr-gs")]), (tag, attrs)):
                self.effecitvePatterns["definition"]["value"] += "->"
            self.history = ""
         
    def handle_endtag(self, tag):    
        #to be fault-tolerant, we ignore tags without ending flag 3 times.
        for i in range(0, 3):
            topTag = self.tagStack.pop()
            if topTag["tag"][0] == tag:
                break
        assert topTag["tag"][0] == tag
        
        #process css format
        self.tagStack.append(topTag)
        if self.IsInPattern("definition"):                
            csStr = self.GetCssString(topTag["tag"])
            self.effecitvePatterns["definition"]["value"] += csStr
        topTag = self.tagStack.pop()
                
        for i in topTag["pattern"]:
            assert i[0] == "effecitvePatterns" or i[0] == "ignoredPatterns"
            if i[0] == "effecitvePatterns":
                self.effecitvePatterns[i[1]]["pattern"][i[2]]["is in"] = False
            else:
                self.ignoredPatterns[i[1]][i[2]]["is in"] = False
            
                
    def handle_data(self, data):      
        #to be fault-tolerant
        if len(self.tagStack) == 0:
            return
        
        #process line break
        for i1 in self.effecitvePatterns:   
            if self.IsInPattern(i1):
                self.history = data
                self.effecitvePatterns[i1]["value"] += data
                break
    
    
    #######################public function    
    #input:
    #   left  = ("xxx|xxx", [("xxx", "xxx")]), "|" is delimiter 
    #   right = ("xxx|xxx", [("xxx", "xxx")]), "|" is delimiter 
    #   only 1 tag could include the delimiter "|"
    def CompareTag(self, left, right):
        if (len(left[1]) == 0 or len(right[1])) == 0:
            return False
        if len(left[1]) > len(right[1]):
            left, right = right, left
        
        if left[0].find("|") == -1:    
            if right[0].find("|") == -1:
                if left[0] != right[0]:
                    return False
            else:
                if left[0] not in right[0].split("|"):
                    return False
        else:
            if right[0].find("|") == -1:
                if right[0] not in left[0].split("|"):
                    return False
            else:
                raise AssertionError
            
        for i in left[1]:
            if i not in right[1]:
                return False
        return True
    
    
    def GetCssString(self, tag):
        csStr = ""
        if self.IsInTagList(self.cssBlockTags, tag):
            csStr = "\n"
        return csStr
    
    
    def GetEffectivePatternsState(self):
        definition = self.effecitvePatterns["definition"]["value"]
        while definition.find("\n \n") != -1:
            definition = definition.replace("\n \n", "\n")
        while definition.find("\n\n") != -1:
            definition = definition.replace("\n\n", "\n")            
        if len(definition) != 0 and definition[0] == "\n":
            definition = definition[1:]
        self.effecitvePatterns["definition"]["value"] = definition
        return self.effecitvePatterns
        
        
    def	GetIgnoredPatternsState(self):
        return self.ignoredPatterns
    
    
    def GetTagStack(self):
        return self.tagStack;

        
    def IsInIgnoredPattern(self):
        for pattern in self.ignoredPatterns:
            if pattern[len(pattern) - 1]["is in"]:
                return True
        return False

        
    def IsInPattern(self, name):
        if self.IsInIgnoredPattern():
            return False
        if name not in self.effecitvePatterns:
            return False
        pattern = self.effecitvePatterns[name]["pattern"]
        return pattern[len(pattern) - 1]["is in"] != 0

        
    def IsInTagList(self, tags, tag):    
        for i in tags:
            if self.CompareTag(i, tag):
                return True
        return False
    
    
    def ReadResult(self):
        effecitvePatterns = self.GetEffectivePatternsState()
        result = []
        result.append(effecitvePatterns["name"]["value"] \
                      + effecitvePatterns["phonetic symbol"]["value"] \
                      + "(word building: #)")
        for i in (effecitvePatterns["word class"]["value"] + " " + effecitvePatterns["definition"]["value"]).split("\n"):
            result.append(i)           
        return result
        
if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-16')
    effecitvePatterns = \
    [
        {
            "pattern name": "name", 
            "pattern": 
            [
                ("div", [("class", "webtop-g")]),
                ("h2", [("class", "h")])
            ]
        },
        {
            "pattern name": "phonetic symbol", 
            "pattern": 
            [
                ("div", [("class", "pron-gs ei-g")]),
                ("span", [("class", "pron-g"), ("geo", "n_am")])
            ]
        },
        {
            "pattern name": "word class", 
            "pattern": 
            [
                ("div", [("class", "webtop-g")]),
                ("span", [("class", "pos")])
            ]
        },
        {
            "pattern name": "definition", 
            "pattern": 
            [
                ("span|li", [("class", "sn-g")])
            ]
        }
    ]
    
    ignoredPatterns = \
    [
        # my ignore list
        [
            ("span", [("class", "collapse")])
        ],
        [
            ("span", [("class", "idm-gs")])
        ],
        [
            ("span", [("class", "pron-g")]),
            ("span", [("class", "prefix")])
        ],        
        [
            ("span", [("class", "sym_first")])
        ],        
        [
            ("span", [("class", "un")])
        ],       
        [
            ("div", [("id", "ox-enlarge")])
        ],
        # disply: none
        [   #css .name format.
            ("span", [("class", "name")])
        ],
        [   #css .pron-gs .wrap format.
            ("div", [("class", "pron-gs ei-g")]),
            ("span", [("class", "wrap")])
        ],
        [   #css .pron-gs .wrap format.
            ("span", [("class", "num")])
        ]
    ]
    
    cssBlockTags = \
    [
        #we do not take cate data between "sn-gs" and "sn-g"
        #("span", [("class", "sn-gs")]),     
        ("span|li", [("class", "sn-g")]), 
        ("span", [("class", "x-gs")]),
        ("span", [("class", "x-g")]), 
        ("span", [("class", "xr-gs")]),
    ]
    
    parser = MyHtmlParser(effecitvePatterns, ignoredPatterns, cssBlockTags)
    assert len(sys.argv) == 2
    srcFileObj = codecs.open(sys.argv[1], "r", "utf-8")

    for line in srcFileObj:
        parser.feed(line)
        
    result = parser.ReadResult()
    for i in result:
        print(i)
    