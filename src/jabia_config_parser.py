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
from collections import namedtuple
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

                   

classKeywords = map(lambda x: Keyword(x), ["Weapon", "Attachment", "Ammunition",
                                           "Clothing", "Collectible", "Consumable",
                                           "Item"])
commonKeywords = map(lambda x: Keyword(x), ["Weight","Price", "Picture", "Icon", "Deliverable"

                                            ])
weaponKeywords = map(lambda x: Keyword(x), ["ResourceId",
                                            "ShotEffectId", "Damage", "BestRange",
                                            "StanceFactor", "Burst", "Auto",
                                            "RPM", "Spread", "ClipSize", "GunType", "Silencing",
                                            "Ammunition", "Quality", "Accuracy", "Aimtime",
                                            "DisableAttachments","AnchorPoint"
                                            
                                            ])
ammoKeywords = map(lambda x: Keyword(x), ["BoxSize", "ArmorFactor", "Projectiles"])
collectibleKeywords = Keyword("StackSize")
clothingKeywords = map(lambda x: Keyword(x), ["CamoUrba", "CamoWoods", "CamoDesert", "Property"])
#TODO clothings.txt not parsed
itemKeywords = map(lambda x: Keyword(x), ["SubType", "Requirement", "Efficiency", "Range", "Charges"])
#TODO consumables.txt not parsed
reservedKeywords = MatchFirst(commonKeywords) | MatchFirst(weaponKeywords) \
                    | MatchFirst(ammoKeywords) | MatchFirst(collectibleKeywords) \
                    | MatchFirst(itemKeywords)
jabiaInteger = Word(nums)
jabiaNumber = Combine( Optional('-') + ( '0' | Word('123456789',nums) ) +
                    Optional( '.' + jabiaInteger ) ) 
jabiaValue = ~reservedKeywords + (jabiaNumber ^ Word(alphanums) ^ Word(alphanums+"_")  )
#print reservedKeywords
jabiaStatement =  Group ( reservedKeywords + Optional( ZeroOrMore(jabiaValue) ) ) # search till next keyword
jabiaObjectFields = ZeroOrMore( jabiaStatement )
jabiaClass = Group( MatchFirst(classKeywords) + LPAR + delimitedList(jabiaInteger ^ Word(alphas) ^ Combine(Word(alphas) + Literal(" ") + jabiaInteger) )  + RPAR )
jabiaObject =  Group( jabiaClass + LBRACE + jabiaObjectFields + RBRACE )
configFileDef = ZeroOrMore(jabiaObject)
configFileDef.ignore(comment)
configFileDef.ignore(QUOTE)
jabiaNumber.setParseAction( convertNumbers )
jabiaInteger.setParseAction( convertNumbers )


class Weapon(object):
    def test(self):
        print "hi"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Not enough arguments"
        sys.exit()
    f = os.path.abspath(sys.argv[1]) 
    results = configFileDef.parseFile(f)
    pprint.pprint(results.asList())
"""    
    weaponList = []
    for each in results.asList():
        d = {}
        for field in each[1:]:
            if len(field) > 1:
                if len(field) == 2:
                    d[field[0]] = field[1]
                else:
                    d[field[0]] = field[1:]
            else:
                d[field[0]] = True
            d["Id"] = each[0][1]
            d["Armament"] = each[0][2]
            obj = namedtuple(each[0][0], d.keys())(*d.values())    
        print obj
        weaponList.append(obj)

    w = Weapon()
    w.test()
    print w.__dict__
    print type(weaponList[0])
    for i in weaponList:
        i.test()
"""
    



