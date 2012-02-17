"""
Created on February 16, 2012

@author: sbobovyc
"""
"""   
    Copyright (C) 2012 Stanislav Bobovych

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
import os
from pyparsing import *

LPAR,RPAR,LBRACK,RBRACK,LBRACE,RBRACE,SEMI,COMMA = map(Suppress, "()[]{};,")
jabiaKeywords = Keyword("Deliverable") ^ Keyword("DisableAttachments")
jabiaObjectType = Word(alphanums + "_") ^ Combine(Word(alphas) + " " + Word(nums))
jabiaVariable = Word(alphas)
jabiaString = dblQuotedString.setParseAction( removeQuotes )
jabiaNumber = Combine( Optional('-') + ( '0' | Word('123456789',nums) ) +
                    Optional( '.' + Word(nums) ) +
                    Optional( Word('eE',exact=1) + Word(nums+'+-',nums) ) )
jabiaValue = jabiaString | jabiaObjectType | jabiaNumber 
jabiaArray = (jabiaNumber + jabiaString) | OneOrMore(jabiaNumber) | OneOrMore(jabiaString)  
#jabiaStatement = Group(jabiaKeywords + ZeroOrMore("*")) | (Group(jabiaVariable + Group(jabiaArray)) ^ Group(jabiaVariable + jabiaValue & ZeroOrMore("*")))
jabiaStatement = Group(jabiaKeywords + ZeroOrMore("*")) | (Group(jabiaVariable + jabiaArray) ^ Group(jabiaVariable + jabiaValue)) #last one does not match properly   
jabiaObject = Group(jabiaObjectType + LPAR + Optional(Group(delimitedList(jabiaValue))) + RPAR +
            LBRACE + Optional(OneOrMore(jabiaStatement)) + RBRACE)
jabiaObjectCollection = OneOrMore(jabiaObject)
jabiaComment = cppStyleComment 
jabiaObject.ignore( jabiaComment )    
jabiaObjectCollection.ignore(jabiaComment)    

def convertNumbers(s,l,toks):
    n = toks[0]
    try:
        return int(n)
    except ValueError, ve:
        return float(n)
jabiaNumber.setParseAction( convertNumbers )

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Not enough arguments"
        sys.exit()
    file = os.path.abspath(sys.argv[1]) 
    test_data = """0 "a" """
    import pprint
#    results = jabiaObject.parseString(test_data)
    results = jabiaArray.parseString(test_data)
    results = jabiaObjectCollection.parseFile(file)
    pprint.pprint(results.asList())

