#! /usr/bin/python3

import fuzzywuzzy import fuzz
import fuzzywuzzy import process


def lmatch(l_dut, l_c2c):
	for sig_c2c_axi in l_c2c:
		for sig in l_dut:
			if fuzz.ratio(list_or_set, sig_c2c_axi) > 50:    #(list_or_set, key_word)
				fuzz.pa






"""
fuzz.ratio(s1, s2)
fuzz.partial_ratio(s1, s2)
fuzz.token_sort_ratio(s1, s2)
fuzz.token_set_ratio(s1, s2)

process.extract("something",list[], limit=2 )  >>> [("a", 90), ("b", 0)]
process.extractOne("something", list[] )          >>> ("a", 45)

"""
