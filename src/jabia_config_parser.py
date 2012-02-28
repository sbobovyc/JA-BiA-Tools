#http://pyparsing.wikispaces.com/file/view/jsonParser.py
#http://pyparsing.wikispaces.com/file/view/oc.py
from pyparsing import *
import pprint

def convertNumbers(s,l,toks):
    n = toks[0]
    try:
        return int(n)
    except ValueError, ve:
        return float(n)
    
# define grammar
jabia_bnf = """
object (id, type)
    { members } 
"""
LPAR,RPAR,LBRACE,RBRACE,COMMA = map(Suppress, "(){},")
jabiaString = dblQuotedString.setParseAction( removeQuotes )
jabiaNumber = Combine( Optional('-') + ( '0' | Word('123456789',nums) ) +
                    Optional( '.' + Word(nums) ) +
                    Optional( Word('eE',exact=1) + Word(nums+'+-',nums) ) )
jabiaObject = Forward()
jabiaValue = Forward()
jabiaVariable = Word(alphas)

jabiaElements = delimitedList( jabiaValue, delim=" " )
jabiaArray = Group(Suppress(' ') + Optional(jabiaElements) + Suppress(' ')) 
jabiaValue << ( jabiaString | jabiaNumber | Group(jabiaObject) )

memberDef = Group( jabiaVariable + jabiaValue) | Group(jabiaVariable + jabiaArray)
jabiaMembers = delimitedList( memberDef, delim=" ") 
jabiaObjectType = Word(alphas)
jabiaObjectId = jabiaNumber
jabiaObjectParameter = jabiaValue | jabiaObjectType
jabiaObject = Group(jabiaObjectType + LPAR + Group(delimitedList(jabiaObjectParameter)) + RPAR + 
                               LBRACE + Optional(jabiaMembers) + RBRACE)

jabiaComment = cppStyleComment 
jabiaObject.ignore( jabiaComment )
jabiaNumber.setParseAction( convertNumbers )

if __name__ == "__main__":
    testdata = """
Weapon (1, test, "testthis"){
//this is a comment
Weight 4300 
//weight 3 4
}"""
#C:\Users\sbobovyc\Desktop\bia\1.03\bin_win32\configs\weapons.txt
    results = jabiaObject.parseString(testdata)
    pprint.pprint( results.asList() )