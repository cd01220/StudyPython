#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-
import codecs
import unittest
import FormatWords

class TestFormatWords(unittest.TestCase):
    def setUp(self):
        self.effecitvePatterns = \
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
        
        self.ignoredPatterns = \
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
        
        self.cssBlockTags = \
        [
            #we do not take cate data between "sn-gs" and "sn-g"
            #("span", [("class", "sn-gs")]),     
            ("span|li", [("class", "sn-g")]), 
            ("span", [("class", "x-gs")]),
            ("span", [("class", "x-g")]), 
            ("span", [("class", "xr-gs")]),
        ]
    
    def test_CompareTag(self):
        left  = ("tag1", [("attr name 1", "attr value 1"), ("attr name 2", "attr value 2")])
        right = ("tag1", [("attr name 1", "attr value 1")])
        parser = FormatWords.MyHtmlParser([], [], [])
        self.assertTrue(parser.CompareTag(left, right))
        
        left  = ("tag1", [("attr name 1", "attr value 1"), ("attr name 2", "attr value 2")])
        right = ("tag1", [("attr name 2", "attr value 2")])
        parser = FormatWords.MyHtmlParser([], [], [])
        self.assertTrue(parser.CompareTag(left, right))
        
        left  = ("tag1|tag2|tag3", [("attr name 1", "attr value 1")])
        right = ("tag2", [("attr name 1", "attr value 1")])
        parser = FormatWords.MyHtmlParser([], [], [])
        self.assertTrue(parser.CompareTag(left, right))
        self.assertTrue(parser.CompareTag(right, left))
            
        left  = ("tag1", [("attr name 1", "attr value 1"), ("attr name 2", "attr value 2")])
        right = ("tag1", [("attr name 3", "attr value 3")])
        parser = FormatWords.MyHtmlParser([], [], [])
        self.assertFalse(parser.CompareTag(left, right))
        
        
    def test_GetInit1(self):
        parser = FormatWords.MyHtmlParser(self.effecitvePatterns, self.ignoredPatterns, self.cssBlockTags)
        result = parser.GetEffectivePatternsState()
        for i1 in self.effecitvePatterns:
            name = i1["pattern name"]
            pattern = i1["pattern"]
            tagNumber = len(pattern)
            self.assertEqual(len(result[name]["pattern"]), tagNumber)
            for i2 in range(0, tagNumber):
                self.assertEqual(result[name]["pattern"][i2]["tags"], pattern[i2])
                self.assertFalse(result[name]["pattern"][i2]["is in"])
    
    
    def test_GetInit2(self):
        parser = FormatWords.MyHtmlParser(self.effecitvePatterns, self.ignoredPatterns, self.cssBlockTags)
        result = parser.GetIgnoredPatternsState()
        self.assertEqual(len(self.ignoredPatterns), len(result))
        for i1 in range(0, len(self.ignoredPatterns)):
            self.assertEqual(len(self.ignoredPatterns[i1]), len(result[i1]))
            for i2 in range(0, len(self.ignoredPatterns[i1])):
                self.assertEqual(self.ignoredPatterns[i1][i2], result[i1][i2]["tags"])
                self.assertFalse(result[i1][i2]["is in"])
    
    
    def test_IsInIgnoredPattern(self):
        parser = FormatWords.MyHtmlParser(self.effecitvePatterns, self.ignoredPatterns, self.cssBlockTags)        
        self.assertFalse(parser.IsInIgnoredPattern())
        parser.handle_starttag("span", [("class", "pron-g")])
        self.assertFalse(parser.IsInIgnoredPattern())
        parser.handle_starttag("span", [("class", "prefix")])
        self.assertTrue(parser.IsInIgnoredPattern())
    
    
    def test_IsInPattern(self):
        parser = FormatWords.MyHtmlParser(self.effecitvePatterns, self.ignoredPatterns, self.cssBlockTags)
        self.assertFalse(parser.IsInPattern("name"))
        parser.handle_starttag("div", [("class", "webtop-g")])
        self.assertFalse(parser.IsInPattern("name"))
        parser.handle_starttag("h2", [("class", "h")])
        self.assertTrue(parser.IsInPattern("name"))
        
    
    def test_Stack1(self): 
        parser = FormatWords.MyHtmlParser(self.effecitvePatterns, self.ignoredPatterns, self.cssBlockTags)
        parser.handle_starttag("div", [("class", "webtop-g")])
        parser.handle_starttag("div", [("class", "pron-gs ei-g")])
        result = parser.GetTagStack()
        expectation = \
        [
            {
                "tag"    : ('div', [('class', 'webtop-g')]), 
                "pattern": [('effecitvePatterns', "name", 0), ('effecitvePatterns', "word class", 0)]
            },
            {
                "tag"    : ('div', [('class', 'pron-gs ei-g')]),
                "pattern": [('effecitvePatterns', "phonetic symbol", 0), ('ignoredPatterns', 7, 0)]
            },
        ]
        self.assertEqual(len(result), len(expectation))
        for i1 in range(0, len(result)):
            self.assertEqual(result[i1]["tag"], expectation[i1]["tag"])
            self.assertEqual(len(result[i1]["pattern"]), len(expectation[i1]["pattern"]))
            for i2 in range(0, len(result[i1]["pattern"])):
                self.assertTrue(result[i1]["pattern"][i2] in expectation[i1]["pattern"])
        
        parser.handle_endtag("div");    
        parser.handle_endtag("div");      
        self.assertEqual(len(result), 0)
                
    def test_Stack2(self):
        parser = FormatWords.MyHtmlParser(self.effecitvePatterns, self.ignoredPatterns, self.cssBlockTags)
        parser.handle_starttag("div", [("class", "pron-gs ei-g")])
        parser.handle_starttag("span", [("class", "wrap")])
        parser.handle_starttag("span", [("class", "xxxx")])
        result = parser.GetTagStack()
        expectation = \
        [
            {
                "tag"    : ('div', [('class', 'pron-gs ei-g')]), 
                "pattern": [('effecitvePatterns', "phonetic symbol", 0), ('ignoredPatterns', 7, 0)]
            },
            {
                "tag"    : ('span', [('class', 'wrap')]), 
                "pattern": [('ignoredPatterns', 7, 1)]
            },
            {
                "tag"    : ('span', [('class', 'xxxx')]), 
                "pattern": []
            }
        ]
        self.assertEqual(result, expectation)  
        
        parser.handle_endtag("span");
        parser.handle_endtag("span");
        parser.handle_endtag("div");
        self.assertEqual(len(result), 0)
    
    
    def test_HandleEndTag1(self):
        parser = FormatWords.MyHtmlParser(self.effecitvePatterns, self.ignoredPatterns, self.cssBlockTags)        
        result = parser.GetEffectivePatternsState()
        expectation = \
        {
            'name': 
            {
                'value': '',
                'pattern': 
                [
                    {
                        'tags': ('div', [('class', 'webtop-g')]), 
                        'is in': False
                    }, 
                    {
                        'tags': ('h2', [('class', 'h')]), 
                        'is in': False
                    }
                ],
            },
            'phonetic symbol': 
            { 
                'value': '',
                'pattern': 
                [
                    {
                        'tags': ('div', [('class', 'pron-gs ei-g')]), 
                        'is in': False
                    }, 
                    {
                        'tags': ("span", [("class", "pron-g"), ("geo", "n_am")]), 
                        'is in': False
                    }
                ],
            },
            'word class': 
            { 
                'value': '',
                'pattern': 
                [
                    {
                        'tags': ("div", [("class", "webtop-g")]), 
                        'is in': False
                    }, 
                    {
                        'tags': ("span", [("class", "pos")]), 
                        'is in': False
                    }
                ],
            },
            'definition': 
            { 
                'value': '',
                'pattern': 
                [
                    {
                        'tags': ("span|li", [("class", "sn-g")]), 
                        'is in': False
                    }
                ],
            }
        }
        self.assertEqual(result, expectation)   
        '''
        parser.handle_starttag("div", [("class", "webtop-g")])
        parser.handle_starttag("h2", [("class", "h")])
        expectation["name"]["pattern"][0]["is in"] = True
        expectation["name"]["pattern"][1]["is in"] = True
        expectation["word class"]["pattern"][0]["is in"] = True
        self.assertEqual(result, expectation)  
        
        parser.handle_endtag("h2");
        expectation["name"]["pattern"][1]["is in"] = False
        self.assertEqual(result, expectation)        
        
        parser.handle_endtag("div");
        expectation["name"]["pattern"][0]["is in"] = True
        expectation["word class"]["pattern"][0]["is in"] = False
        self.assertEqual(result, expectation)
        '''
    
    def test_HandleEndTag2(self):
        ignoredPatterns = \
        [
            [
                ("span1", [("class", "ignore1")]),
                ("span1", [("class", "ignore2")])
            ],
            [
                ("span2", [("class", "ignore1")]),
                ("span2", [("class", "ignore2")])
            ]
        ]
        parser = FormatWords.MyHtmlParser([], ignoredPatterns, [])
        
        result = parser.GetIgnoredPatternsState()
        expectation = \
        [
            [
                {
                    "tags": ("span1", [("class", "ignore1")]), 
                    "is in": False
                },
                {
                    "tags": ("span1", [("class", "ignore2")]), 
                    "is in": False
                }
            ],
            [
                {
                    "tags": ("span2", [("class", "ignore1")]), 
                    "is in": False
                },
                {
                    "tags": ("span2", [("class", "ignore2")]), 
                    "is in": False
                }
            ]
        ]
        self.assertEqual(result, expectation)        
        
        parser.handle_starttag("span1", [("class", "ignore1")])
        parser.handle_starttag("span2", [("class", "ignore2")])
        parser.handle_starttag("span2", [("class", "ignore1")])
        expectation[0][0]["is in"] = True
        expectation[1][0]["is in"] = True
        self.assertEqual(result, expectation)          
        
        parser.handle_endtag("span2");
        expectation[1][0]["is in"] = False
        self.assertEqual(result, expectation)         
        
        parser.handle_endtag("span2");
        parser.handle_endtag("span1");
        expectation[0][0]["is in"] = False
        self.assertEqual(result, expectation) 
    
    
    def test_HandleData(self):
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
                "pattern name": "word class", 
                "pattern":
                [
                    ("div", [("class", "webtop-g")]),
                    ("span", [("class", "pos")]), 
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
        parser = FormatWords.MyHtmlParser(effecitvePatterns, [], [])
        
        parser.handle_starttag("div", [("class", "webtop-g")])
        parser.handle_starttag("h2", [("class", "h")])
        parser.handle_data("xxxxxxxxxxx")
        parser.handle_endtag("h2");
        parser.handle_starttag("span", [("class", "pos")])
        parser.handle_data("yyyyyyyyyyyyy")
        
        result = parser.GetEffectivePatternsState()
        self.assertEqual(result["name"]["value"], "xxxxxxxxxxx")
        self.assertEqual(result["word class"]["value"], "yyyyyyyyyyyyy")
        
    
    def test_HandleStartTag1(self):
        effecitvePatterns = \
        [
            {
                "pattern name": "name", 
                "pattern": 
                [
                    ("span1", [("class", "xxx1")]),
                    ("span1", [("class", "xxx2")])
                ]
            },            
            {
                "pattern name": "phon", 
                "pattern": 
                [
                    ("span1", [("class", "xxx1")]),
                    ("span1", [("class", "xxx3")])
                ]
            },
            {
                "pattern name": "definition", 
                "pattern": 
                [
                    ("span", [("class", "sn-g")])
                ]
            }
        ]
        parser = FormatWords.MyHtmlParser(effecitvePatterns, [], [])
        
        result = parser.GetEffectivePatternsState()
        expectation = \
        {
            'name': 
            {
                'value': '',
                'pattern': 
                [
                    {
                        'tags': ('span1', [('class', 'xxx1')]), 
                        'is in': False
                    }, 
                    {
                        'tags': ('span1', [('class', 'xxx2')]), 
                        'is in': False
                    }
                ],
            },
            'phon': 
            { 
                'value': '',
                'pattern': 
                [
                    {
                        'tags': ('span1', [('class', 'xxx1')]), 
                        'is in': False
                    }, 
                    {
                        'tags': ('span1', [('class', 'xxx3')]), 
                        'is in': False
                    }
                ],
            },
            'definition': 
            { 
                'value': '',
                'pattern': 
                [
                    {
                        'tags': ("span", [("class", "sn-g")]), 
                        'is in': False
                    }
                ],
            }
        }
        self.assertEqual(result, expectation)   
        
        parser.handle_starttag("span1", [("class", "xxx1")])
        expectation["name"]["pattern"][0]["is in"] = True
        expectation["phon"]["pattern"][0]["is in"] = True
        self.assertEqual(result, expectation)  
        
        parser.handle_starttag("span1", [("class", "xxx3")])
        expectation["phon"]["pattern"][1]["is in"] = True
        self.assertEqual(result, expectation)  
        
        
    def test_HandleStartTag2(self):
        ignoredPatterns = \
        [
            [
                ("span1", [("class", "ignore1")]),
                ("span1", [("class", "ignore2")])
            ],
            [
                ("span2", [("class", "ignore1")]),
                ("span2", [("class", "ignore2")])
            ]
        ]
        parser = FormatWords.MyHtmlParser([], ignoredPatterns, [])
        result = parser.GetIgnoredPatternsState()
        expectation = \
        [
            [
                {
                    "tags": ("span1", [("class", "ignore1")]), 
                    "is in": False
                },
                {
                    "tags": ("span1", [("class", "ignore2")]), 
                    "is in": False
                }
            ],
            [
                {
                    "tags": ("span2", [("class", "ignore1")]), 
                    "is in": False
                },
                {
                    "tags": ("span2", [("class", "ignore2")]), 
                    "is in": False
                }
            ]
        ]
        self.assertEqual(result, expectation)        
        
        parser.handle_starttag("span1", [("class", "ignore1")])
        expectation[0][0]["is in"] = True
        self.assertEqual(result, expectation)  
        
        parser.handle_starttag("span2", [("class", "ignore2")])
        self.assertEqual(result, expectation)  
        
        parser.handle_starttag("span2", [("class", "ignore1")])
        expectation[1][0]["is in"] = True
        self.assertEqual(result, expectation)  
        
        parser.handle_starttag("span1", [("class", "ignore2")])
        expectation[0][1]["is in"] = True
        self.assertEqual(result, expectation)          
    
    
    def test_WordOfLook(self):               
        resultCommence = """look /lʊk/ (word building: #)
            verb 1 [intransitive] to turn your eyes in a particular direction
            : If you look carefully you can just see our house from here.
            : look (at somebody/something) She looked at me and smiled.
            : ‘Has the mail come yet?’ ‘I'll look and see.’
            : Look! I'm sure that's Brad Pitt!
            : Don't look now, but there's someone staring at you!
            ->see also forward-looking
            2 [intransitive] to try to find somebody/something
            : I can't find my book—I've looked everywhere.
            : look for somebody/something Where have you been? We've been looking for you.
            : Are you still looking for a job?
            : We’re looking for someone with experience for this post.
            3 [intransitive, transitive] to pay attention to something
            : look (at something) Look at the time! We're going to be late.
            : look where, what, etc… Can't you look where you're going?
            4 linking verb to seem; to appear
            : + adj. to look pale/happy/tired
            : That book looks interesting.
            : look (to somebody) like somebody/something That looks like an interesting book.
            : + noun That looks an interesting book.
            : You made me look a complete fool!
            ->see also good-looking
            5 [intransitive] (not usually used in the progressive tenses) to have a similar appearance to somebody/something; to have an appearance that suggests that something is true or will happen
            : look (to somebody) like somebody/something That photograph doesn't look like her at all.
            : It looks like rain (= it looks as if it's going to rain).
            : look (to somebody) as if…/as though… You look as though you slept badly.
            : They don’t look like they’re trying to win.
            6 [intransitive] to seem likely
            : look (to somebody) as if…/as though… It doesn't look as if we'll be moving after all.
             look (to somebody) like… (informal)
            : It doesn't look like we'll be moving after all.
            7 [intransitive] + adv./prep. to face a particular direction
            : The house looks east.
            : The hotel looks out over the harbour.
            """
        left = resultCommence.splitlines()
        parser = FormatWords.MyHtmlParser(self.effecitvePatterns, self.ignoredPatterns, self.cssBlockTags)
        srcFileObj = codecs.open("./UnitTestFiles/look.html", "r", "utf-8")
        for line in srcFileObj:
            parser.feed(line)
        right = parser.ReadResult()
        self.assertEqual(len(left), len(right))
        for i in range(0, len(left)):
            self.assertEqual(left[i].lstrip(), right[i].lstrip())
        srcFileObj.close()
        
        
    def test_WordOfBlason(self):               
        resultCommence = """blazon /ˈbleɪzn/ (word building: #)
            verb 1 [usually passive] blazon something (on/across/over something) 
            ->= emblazon
            : He had the word ‘Cool’ blazoned across his chest.
            2 ->= blaze (4)
            """
        left = resultCommence.splitlines()
        parser = FormatWords.MyHtmlParser(self.effecitvePatterns, self.ignoredPatterns, self.cssBlockTags)
        srcFileObj = codecs.open("./UnitTestFiles/blazon.html", "r", "utf-8")
        for line in srcFileObj:
            parser.feed(line)
        right = parser.ReadResult()
        self.assertEqual(len(left), len(right))
        for i in range(0, len(left)):
            self.assertEqual(left[i].lstrip(), right[i].lstrip())
        srcFileObj.close()
    
    
    def test_WordOfBead(self):               
        resultCommence = """bead /biːd/ (word building: #)
            noun 1  [countable] a small piece of glass, wood, etc. with a hole through it, that can be put on a string with others of the same type and worn as jewellery, etc.
            : a necklace of wooden beads
            : A bead curtain separated the two rooms.
            ->see also worry beads
            ->See related entries: Jewellery
            2  beads [plural] a rosary
            : In one of the pews a woman was fingering her beads.
            3 [countable] a small drop of liquid
            : There were beads of sweat on his forehead.
            """
        left = resultCommence.splitlines()
        parser = FormatWords.MyHtmlParser(self.effecitvePatterns, self.ignoredPatterns, self.cssBlockTags)
        srcFileObj = codecs.open("./UnitTestFiles/bead.html", "r", "utf-8")
        for line in srcFileObj:
            parser.feed(line)
        right = parser.ReadResult()
        self.assertEqual(len(left), len(right))
        for i in range(0, len(left)):
            self.assertEqual(left[i].lstrip(), right[i].lstrip())
        srcFileObj.close()
        
        
    def test_WordOfCommence(self):               
        resultCommence = """commence /kəˈmens/ (word building: #)
            verb 1 to begin to happen; to begin something
            : The meeting is scheduled to commence at noon.
            : I will be on leave during the week commencing 15 February.
            : commence with something The day commenced with a welcome from the principal.
            : commence something She commenced her medical career in 1956.
            : The company commenced operations in April.
            : to commence bankruptcy proceedings against somebody
            : commence doing something We commence building next week.
            : commence to do something Operators commenced to build pipelines in 1862.
            ->See related entries: Business meetings
            """
        left = resultCommence.splitlines()
        parser = FormatWords.MyHtmlParser(self.effecitvePatterns, self.ignoredPatterns, self.cssBlockTags)
        srcFileObj = codecs.open("./UnitTestFiles/commence.html", "r", "utf-8")
        for line in srcFileObj:
            parser.feed(line)
        right = parser.ReadResult()
        self.assertEqual(len(left), len(right))
        for i in range(0, len(left)):
            self.assertEqual(left[i].lstrip(), right[i].lstrip())
        srcFileObj.close()
        
           
    def test_WordOfCompetent(self):               
        resultCommence = """competent /ˈkɑːmpɪtənt/ (word building: #)
            adjective 1 having enough skill or knowledge to do something well or to the necessary standard
            : Make sure the firm is competent to carry out the work.
            : He's very competent in his work.
            : I don’t feel competent to comment.
            ->opposite incompetent
            ->See related entries: Clever, Job skills and personal qualities
            2 of a good standard but not very good
            3 having the power to decide something
            : The case was referred to a competent authority.
            """
        left = resultCommence.splitlines()
        parser = FormatWords.MyHtmlParser(self.effecitvePatterns, self.ignoredPatterns, self.cssBlockTags)
        srcFileObj = codecs.open("./UnitTestFiles/competent.html", "r", "utf-8")
        for line in srcFileObj:
            parser.feed(line)
        right = parser.ReadResult()
        self.assertEqual(len(left), len(right))
        for i in range(0, len(left)):
            self.assertEqual(left[i].lstrip(), right[i].lstrip())
        srcFileObj.close()
        
        
    def test_WordOfIdeology(self):               
        resultCommence = """ideology /ˌaɪdiˈɑːlədʒi/ (word building: #)
            noun 1 a set of ideas that an economic or political system is based on
            : Marxist/capitalist ideology
            2 a set of beliefs, especially one held by a particular group, that influences the way people behave
            : the ideology of gender roles
            : alternative ideologies
            """
        left = resultCommence.splitlines()
        parser = FormatWords.MyHtmlParser(self.effecitvePatterns, self.ignoredPatterns, self.cssBlockTags)
        srcFileObj = codecs.open("./UnitTestFiles/ideology.html", "r", "utf-8")
        for line in srcFileObj:
            parser.feed(line)
        right = parser.ReadResult()
        self.assertEqual(len(left), len(right))
        for i in range(0, len(left)):
            self.assertEqual(left[i].lstrip(), right[i].lstrip())
        srcFileObj.close()
        
        
    def test_WordOfWelfare(self):               
        resultCommence = """welfare /ˈwelfer/ (word building: #)
            noun 1 the general health, happiness and safety of a person, an animal or a group 
            ->synonym well-being
            : We are concerned about the child's welfare.
            2 practical or financial help that is provided, often by the government, for people or animals that need it
            : The state is still the main provider of welfare.
            : child welfare
            : a social welfare programme
            : welfare provision/services/work
            ->See related entries: Helping others
            3 (especially North American English) (British English also social security) money that the government pays regularly to people who are poor, unemployed, sick, etc.
            : They would rather work than live on welfare.
            ->See related entries: Helping others
            """
        left = resultCommence.splitlines()
        parser = FormatWords.MyHtmlParser(self.effecitvePatterns, self.ignoredPatterns, self.cssBlockTags)
        srcFileObj = codecs.open("./UnitTestFiles/welfare.html", "r", "utf-8")
        for line in srcFileObj:
            parser.feed(line)
        right = parser.ReadResult()
        self.assertEqual(len(left), len(right))
        for i in range(0, len(left)):
            self.assertEqual(left[i].lstrip(), right[i].lstrip())
        srcFileObj.close()
        
        
    def tearDown(self):
        pass      
        
if __name__ == '__main__':
    unittest.main()
