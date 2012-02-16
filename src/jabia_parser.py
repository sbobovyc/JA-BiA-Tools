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
from pyparsing import *

LPAR,RPAR,LBRACK,RBRACK,LBRACE,RBRACE,SEMI,COMMA = map(Suppress, "()[]{};,")
jabiaKeywords = Keyword("Deliverable") ^ Keyword("DisableAttachments")
jabiaObjectType = Word(alphanums + "_")
jabiaVariable = Word(alphas)
jabiaString = dblQuotedString.setParseAction( removeQuotes )
jabiaNumber = Combine( Optional('-') + ( '0' | Word('123456789',nums) ) +
                    Optional( '.' + Word(nums) ) +
                    Optional( Word('eE',exact=1) + Word(nums+'+-',nums) ) )
jabiaValue = jabiaString | jabiaObjectType | jabiaNumber
#jabiaArray = delimitedList(jabiaNumber, delim=White(' ',exact=1)) 
jabiaArray = OneOrMore(jabiaNumber)
jabiaStatement = Group(jabiaKeywords + ZeroOrMore("*")) | (Group(jabiaVariable + jabiaArray) ^ Group(jabiaVariable + jabiaValue))   
#jabiaObject = OneOrMore(jabiaStatement)
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
    test_data = """
// 38 S&W
Weapon (36, HandGun)
{
    Weight 650
      Price 720
    ResourceId 4205    
    ShotEffectId 5608

    // logic:
    Damage 22
    BestRange 14.0
    StanceFactor 0 1
    StanceFactor 1 0.9
    StanceFactor 2 0.9
    StanceFactor 3 0.9
    ClipSize 6
    Ammunition 38cal
    Quality 400
    RPM 450
      GunType Handgun
    Icon 0 112 200 112 40
    Picture 0 8 0 2
    
    
    DisableAttachments
    AnchorPoint 0.0 0.5 -1.9
    
    Deliverable
}
"""
    import pprint
#    results = jabiaObject.parseString(test_data)
#    pprint.pprint( results.asList() )
    results = jabiaObjectCollection.parseFile("C:\\Users\\sbobovyc\\Desktop\\test\\bin_win32\\configs\\weapons.txt")
    pprint.pprint(results.asList())

