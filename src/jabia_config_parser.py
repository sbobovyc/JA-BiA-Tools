"""
Created on October 16, 2014

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
import pprint
import sys
import os
from pyparsing import *


def convertNumbers(s,l,toks):
    n = toks[0]    
    try:
        return int(n)
    except ValueError, ve:
        return float(n)

LPAR,RPAR,LBRACK,RBRACK,LBRACE,RBRACE,SEMI,COMMA,QUOTE = map(Suppress, "()[]{};,'")
newline = Suppress(LineEnd())
comment = cppStyleComment

                   

classKeywords = map(lambda x: Keyword(x), ["Weapon", "Attachment"])
weaponKeywords = map(lambda x: Keyword(x), ["Weight", "Price", "ResourceId",
                                            "ShotEffectId", "Damage", "BestRange",
                                            "StanceFactor", "Burst", "Auto",
                                            "RPM", "Spread", "ClipSize", "GunType",
                                            "Ammunition", "Quality", "Icon",
                                            "Picture", "DisableAttachments","AnchorPoint",
                                            "Deliverable"
                                            ])
reservedKeywords = MatchFirst(weaponKeywords)
jabiaInteger = Word(nums)
jabiaNumber = Combine( Optional('-') + ( '0' | Word('123456789',nums) ) +
                    Optional( '.' + jabiaInteger ) ) 
jabiaValue = ~reservedKeywords + (jabiaNumber ^ Word(alphanums) ^ Word(alphanums+"_")  )
#print reservedKeywords
jabiaStatement =  Group ( reservedKeywords + Optional( ZeroOrMore(jabiaValue) ) )
jabiaObjectFields = ZeroOrMore( jabiaStatement )
jabiaClass = Group( MatchFirst(classKeywords) + LPAR + delimitedList(jabiaInteger ^ Word(alphas) ^ Combine(Word(alphas) + Literal(" ") + jabiaInteger) )  + RPAR )
jabiaObject =  Group( jabiaClass + LBRACE + jabiaObjectFields + RBRACE )
configFileDef = ZeroOrMore(jabiaObject)
configFileDef.ignore(comment)
configFileDef.ignore(QUOTE)
jabiaNumber.setParseAction( convertNumbers )
jabiaInteger.setParseAction( convertNumbers )



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Not enough arguments"
        sys.exit()
    f = os.path.abspath(sys.argv[1]) 
    results = configFileDef.parseFile(f)
    pprint.pprint(results.asList())



