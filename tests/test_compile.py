"""Tests for regex/test_compile.py"""

import unittest as ut
from regex.compile import CompiledRegex, Match


class CompileTest(ut.TestCase):

    def test_match(self):
        reg = CompiledRegex(r"a+b+")
        text = "aaaaabbbbaaababaaaabbbb"
        self.assertEqual(
            reg.match(text),
            Match(text, (0, 9))
        )
        reg = CompiledRegex(r"[ab]*c[ab]*")
        text = "aaaaabbbbaacababdaaaabbbb"
        self.assertEqual(
            reg.match(text),
            Match(text, (0, 16))
        )
        reg = CompiledRegex(r"\s*(www\.)?[-a-zA-Z]+\.")
        text = "   www.Git-Hub.com.pl"
        self.assertEqual(
            reg.match(text),
            Match(text, (0, 15))
        )
        text = " Git-Hub.com.pl"
        self.assertEqual(
            reg.match(text),
            Match(text, (0, 9))
        )
        reg = CompiledRegex(r"a+b+")
        text = "www.Git-Hub.com.pl"
        self.assertEqual(
            None,
            reg.match(text)
        )
        reg = CompiledRegex(r"a*b*")
        text = "www.Git-Hub.com.pl"
        self.assertEqual(
            reg.match(text),
            Match(text, (0, 0))
        )
        reg = CompiledRegex(r"a[]a")
        text = "aa aaa aaaa"
        self.assertEqual(
            reg.match(text),
            None
        )
        reg = CompiledRegex(r"a()a")
        text = "aa aaa aaaa"
        self.assertEqual(
            reg.match(text),
            None
        )

    def test_find_iter(self):
        reg = CompiledRegex(r"a+b+")
        text = """
aaaabbbaaab
aabbaaabbb
abbab
"""
        self.assertEqual(
            reg.find_all(text),
            [
                Match(text, (1, 8)),
                Match(text, (8, 12)),
                Match(text, (13, 17)),
                Match(text, (17, 23)),
                Match(text, (24, 27)),
                Match(text, (27, 29)),
            ]
        )
        reg = CompiledRegex(r"a*b*")
        text = """
aaaabbbaaab
aabbaaabbb
abbab
"""
        self.assertEqual(
            reg.find_all(text),
            [
                Match(text, (0, 0)),
                Match(text, (1, 8)),
                Match(text, (8, 12)),
                Match(text, (12, 12)),
                Match(text, (13, 17)),
                Match(text, (17, 23)),
                Match(text, (23, 23)),
                Match(text, (24, 27)),
                Match(text, (27, 29)),
                Match(text, (29, 29)),
            ]
        )
        reg = CompiledRegex(r"([a-z0-9_\.]+)@([-\da-z\.]+)\.([a-z\.]{2,6})")
        text = '''
adam.kowalski@gmail.pl
grzegorz_brzeczyszczykiewicz@icloud.com
walter1978white@mk.pl
notAnEmail@gmail.io
notanemailalsogmail.com
'''
        self.assertEqual(
            reg.find_all(text),
            [
                Match(text, (1, 23)),
                Match(text, (24, 63)),
                Match(text, (64, 85)),
                Match(text, (92, 105)),
            ]
        )
        reg = CompiledRegex(r"b[ab]*")
        text = 'aabbbbbaaabbaaabbbba'
        self.assertEqual(
            reg.find_all(text),
            [
                Match(text, (2, len(text)))
            ]
        )
        reg = CompiledRegex(r".*")
        text = 'ocwei uhwp98y24p985h;i4ubv;wej wv fkjew '
        self.assertEqual(
            reg.find_all(text),
            [
                Match(text, (0, len(text)))
            ]
        )
        reg = CompiledRegex(r"|")
        text = 'ocw'
        self.assertEqual(
            reg.find_all(text),
            [
                Match(text, (0, 0)),
                Match(text, (1, 1)),
                Match(text, (2, 2))
            ]
        )

    def test_match_full(self):
        reg = CompiledRegex(r"ocw")
        text = 'ocw'
        self.assertTrue(reg.full_match(text) is not None)
        reg = CompiledRegex(r"a+b+")
        text = 'aaaaaabbbbbbb'
        self.assertTrue(reg.full_match(text) is not None)
        reg = CompiledRegex(r"a+b+")
        text = 'aaaaaabbbbbbba'
        self.assertTrue(reg.full_match(text) is None)
        reg = CompiledRegex(r"([a-z0-9_\.]+)@([-\da-z\.]+)\.([a-z\.]{2,6})")
        text = 'suspicious_tech_support@not-a-scam.edu.pl'
        self.assertTrue(reg.full_match(text) is not None)
        reg = CompiledRegex(r"([a-z0-9_\.]+)@([-\da-z\.]+)\.([a-z\.]{2,6})")
        text = 'normal_email_addressATgmail.com'
        self.assertTrue(reg.full_match(text) is None)
        reg = CompiledRegex(r"(www\.)?[-A-Za-z0-9_\.]+\.(com|pl|io)")
        text = 'www.website_ai.pl.com'
        self.assertTrue(reg.full_match(text) is not None)
        reg = CompiledRegex(r"(www\.)?[-A-Za-z0-9_\.]+\.(com|pl|io)")
        text = 'website_ai.pl.com'
        self.assertTrue(reg.full_match(text) is not None)
        reg = CompiledRegex(r"(www\.)?[-A-Za-z0-9_\.]+\.(com|pl|io)")
        text = 'www.website_ai.pl.co'
        self.assertTrue(reg.full_match(text) is None)

    def test_search(self):
        reg = CompiledRegex(r"(www\.)?[-A-Za-z0-9_\.]+\.(com|pl|io)")
        text = 'this is my website: www.website_ai.pl.co end of website'
        self.assertEqual(
            reg.search(text),
            Match(text, (20, 37))
        )
        reg = CompiledRegex(r"\s(www\.)?[-A-Za-z0-9_\.]+\.(com|pl|io)")
        text = 'this is my email: walter_bialy@gmail.com end of email'
        self.assertEqual(
            reg.search(text),
            None
        )
        reg = CompiledRegex(r"a+")
        text = 'bbbbbbbbaaaaaa'
        self.assertEqual(
            reg.search(text),
            Match(text, (8, 14))
        )
        reg = CompiledRegex(r"a+")
        text = 'aaabbbbbbbaaaaaaaabbbbaaaaaaaaaaaaaa'
        self.assertEqual(
            reg.search(text),
            Match(text, (0, 3))
        )
        reg = CompiledRegex(r"a+")
        text = 'aaabbbbbbbaaaaaaaabbbbaaaaaaaaaaaaaa'
        self.assertEqual(
            reg.search(text),
            Match(text, (0, 3))
        )
        reg = CompiledRegex(r"g[a-zA-Z]*d")
        text = """
        According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small 
        to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans
        think is impossible. Yellow, black. Yellow, black. Yellow, black. Yellow, black. Ooh, black and yellow!"""
        self.assertEqual(
            reg.search(text),
            Match(text, (163, 169))
        )
        reg = CompiledRegex(r"\sy[a-zA-Z]*o\s")
        text = """
        According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small 
        to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans
        think is impossible. Yellow, black. Yellow, black. Yellow, black. Yellow, black. Ooh, black and yellow! yoo """
        self.assertEqual(
            reg.search(text),
            Match(text, (351, 356))
        )
        reg = CompiledRegex(r"this is not in the text")
        self.assertEqual(
            reg.search(text),
            None
        )
        reg = CompiledRegex(r"what humans\n        think is impossible")
        self.assertEqual(
            reg.search(text),
            Match(text, (228, 267))
        )
        reg = CompiledRegex(r"a*")
        text = ' '
        self.assertEqual(
            reg.search(text),
            Match(text, (0, 0))
        )
