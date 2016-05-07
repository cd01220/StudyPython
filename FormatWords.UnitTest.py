import os
import io
import sys  
import codecs
import unittest
import FormatWords


class TestFormatWords(unittest.TestCase):
    def setUp(self):
        pass
                
    def test_WordOfCommence(self):               
        resultCommence = """commence/kəˈmens/(word building: #)
            verb. 1 [intransitive,transitive] to begin to happen; to begin something
            : The meeting is scheduled to commence at noon.
            : I will be on leave during the week commencing 15 February.
            : commence with something The day commenced with a welcome from the principal.
            : commence something She commenced her medical career in 1956.
            : The company commenced operations in April.
            : to commence bankruptcy proceedings against somebody
            : commence doing something We commence building next week.
            : commence to do something Operators commenced to build pipelines in 1862."""
        left = resultCommence.splitlines()
        parser = FormatWords.MyHtmlParser()
        srcFileObj = codecs.open("./UnitTestFiles/commence.html", "r", "utf-8")
        for line in srcFileObj:
            parser.feed(line)
        right = parser.ReadResult()
        self.assertEqual(len(left), len(right))
        for i in range(0, len(left)):
            self.assertEqual(left[i].lstrip(), right[i])
        srcFileObj.close()
        
    def test_WordOfLook(self):               
        resultCommence = """look/lʊk/(word building: #)
            verb. 1 [intransitive] to turn your eyes in a particular direction
            : If you look carefully you can just see our house from here.
            : look (at somebody/something) She looked at me and smiled.
            : ‘Has the mail come yet?’ ‘I'll look and see.’
            : Look! I'm sure that's Brad Pitt!
            : Don't look now, but there's someone staring at you!
            2 [intransitive] to try to find somebody/something
            : I can't find my book—I've looked everywhere.
            : look for somebody/something Where have you been? We've been looking for you.
            : Are you still looking for a job?
            : We’re looking for someone with experience for this post.
            3 [intransitive,transitive] to pay attention to something
            : look (at something) Look at the time! We're going to be late.
            : look where, what, etc… Can't you look where you're going?
            4 [] linking verb to seem; to appear
            : + adj. to look pale/happy/tired
            : That book looks interesting.
            : look (to somebody) like somebody/something That looks like an interesting book.
            : + noun That looks an interesting book.
            : You made me look a complete fool!
            5 [intransitive] (not usually used in the progressive tenses) to have a similar appearance to somebody/something; to have an appearance that suggests that something is true or will happen
            : look (to somebody) like somebody/something That photograph doesn't look like her at all.
            : It looks like rain (= it looks as if it's going to rain).
            : look (to somebody) as if…/as though… You look as though you slept badly.
            : They don’t look like they’re trying to win.
            6 [intransitive] to seem likely
            : look (to somebody) as if…/as though… It doesn't look as if we'll be moving after all.
            : look (to somebody) like… It doesn't look like we'll be moving after all.
            7 [intransitive] + adv./prep. to face a particular direction
            : The house looks east.
            : The hotel looks out over the harbour."""
        left = resultCommence.splitlines()
        parser = FormatWords.MyHtmlParser()
        srcFileObj = codecs.open("./UnitTestFiles/look.html", "r", "utf-8")
        for line in srcFileObj:
            parser.feed(line)
        right = parser.ReadResult()
        self.assertEqual(len(left), len(right))
        for i in range(0, len(left)):
            self.assertEqual(left[i].lstrip(), right[i])
        srcFileObj.close()
    
    def test_WordOfBlazon(self):               
        resultCommence = """blazon/ˈbleɪzn/(word building: #)
            verb. 1 [usually passive] blazon something (on/across/over something) 
            : He had the word ‘Cool’ blazoned across his chest."""
        left = resultCommence.splitlines()
        parser = FormatWords.MyHtmlParser()
        srcFileObj = codecs.open("./UnitTestFiles/blazon.html", "r", "utf-8")
        for line in srcFileObj:
            parser.feed(line)
        right = parser.ReadResult()
        self.assertEqual(len(left), len(right))
        for i in range(0, len(left)):
            self.assertEqual(left[i].lstrip(), right[i])
        srcFileObj.close()
    
    def test_WordOfIdeology(self):               
        resultCommence = """ideology/ˌaɪdiˈɑːlədʒi/(word building: #)
            noun. 1 [countable,uncountable] a set of ideas that an economic or political system is based on
            : Marxist/capitalist ideology
            2 [] a set of beliefs, especially one held by a particular group, that influences the way people behave
            : the ideology of gender roles
            : alternative ideologies"""
        left = resultCommence.splitlines()
        parser = FormatWords.MyHtmlParser()
        srcFileObj = codecs.open("./UnitTestFiles/ideology.html", "r", "utf-8")
        for line in srcFileObj:
            parser.feed(line)
        right = parser.ReadResult()
        self.assertEqual(len(left), len(right))
        for i in range(0, len(left)):
            self.assertEqual(left[i].lstrip(), right[i])
        srcFileObj.close()
        
    def test_WordOfCompetent(self):               
        resultCommence = """competent/ˈkɑːmpɪtənt/(word building: #)
            adjective. 1 [] having enough skill or knowledge to do something well or to the necessary standard
            : Make sure the firm is competent to carry out the work.
            : He's very competent in his work.
            : I don’t feel competent to comment.
            2 [] of a good standard but not very good
            3 [] having the power to decide something
            : The case was referred to a competent authority."""
        left = resultCommence.splitlines()
        parser = FormatWords.MyHtmlParser()
        srcFileObj = codecs.open("./UnitTestFiles/competent.html", "r", "utf-8")
        for line in srcFileObj:
            parser.feed(line)
        right = parser.ReadResult()
        self.assertEqual(len(left), len(right))
        for i in range(0, len(left)):
            self.assertEqual(left[i].lstrip(), right[i])
        srcFileObj.close()
            
    def test_WordOfWelfare(self):               
        resultCommence = """welfare/ˈwelfer/(word building: #)
        noun. 1 [uncountable] the general health, happiness and safety of a person, an animal or a group
        : We are concerned about the child's welfare.
        2 [] practical or financial help that is provided, often by the government, for people or animals that need it
        : The state is still the main provider of welfare.
        : child welfare
        : a social welfare programme
        : welfare provision/services/work
        3 [] money that the government pays regularly to people who are poor, unemployed, sick, etc.
        : They would rather work than live on welfare."""
        left = resultCommence.splitlines()
        parser = FormatWords.MyHtmlParser()
        srcFileObj = codecs.open("./UnitTestFiles/﻿welfare.html", "r", "utf-8")
        for line in srcFileObj:
            parser.feed(line)
        right = parser.ReadResult()
        self.assertEqual(len(left), len(right))
        for i in range(0, len(left)):
            self.assertEqual(left[i].lstrip(), right[i])
        srcFileObj.close()
               
    def test_WordOfBead(self):               
        resultCommence = """bead/biːd/(word building: #)
            noun. 1 [countable] a small piece of glass, wood, etc. with a hole through it, that can be put on a string with others of the same type and worn as jewellery, etc.
            : a necklace of wooden beads
            : A bead curtain separated the two rooms.
            2 [plural] a rosary
            : In one of the pews a woman was fingering her beads.
            3 [countable] a small drop of liquid
            : There were beads of sweat on his forehead."""
        left = resultCommence.splitlines()
        parser = FormatWords.MyHtmlParser()
        srcFileObj = codecs.open("./UnitTestFiles/bead.html", "r", "utf-8")
        for line in srcFileObj:
            parser.feed(line)
        right = parser.ReadResult()
        self.assertEqual(len(left), len(right))
        for i in range(0, len(left)):
            self.assertEqual(left[i].lstrip(), right[i])
        srcFileObj.close()
        
    def tearDown(self):
        pass      
        
if __name__ == '__main__':
    unittest.main()
