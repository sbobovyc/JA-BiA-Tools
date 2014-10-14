import pprint
from pyparsing import \
    Literal,Word,alphas,nums,OneOrMore,ZeroOrMore,Group,cppStyleComment,Combine,Optional,Suppress,LineEnd,LineStart,delimitedList,dblQuotedString

def convertNumbers(s,l,toks):
    n = toks[0]
    try:
        return int(n)
    except ValueError, ve:
        return float(n)

lbrack = Literal("[").suppress()
rbrack = Literal("]").suppress()
rparan = Literal(")").suppress()
lparan = Literal("(").suppress()
lbrace = Literal("{").suppress()
rbrace = Literal("}").suppress()
comma = Literal(",").suppress()
quote = Literal("\"").suppress()
newline = Suppress(LineEnd())
comment = cppStyleComment

number = Combine( Optional('-') + ( '0' | Word('123456789',nums) ) +
                    Optional( '.' + Word(nums) ) ) 
value = number | Word(alphas)                     
statementDef = Group ( Word(alphas) + OneOrMore( number ) ) + newline 
bodyDef = ZeroOrMore( statementDef )
#classObj = Group( Word(alphas) + lparan + Word(nums) + comma + Word(alphas) + Optional( Word(nums) ) + rparan )
classObj = Group( Word(alphas) + lparan + delimitedList(Word(nums) ^ Word(alphas) ^ Combine(Word(alphas) + Literal(" ") + Word(nums)) )  + rparan )
classDef = classObj + lbrace + bodyDef + rbrace
classDef.ignore(comment)
classDef.ignore(quote)
number.setParseAction( convertNumbers )

testString = """Class (45, id 53, "etst") {
//this is a comment
TestA 3 2
TestB 5.3 -6.6
}"""

testString2 = """
// SCAR-L Urban
Weapon (70, Rifle) {
Weight 400
Price 400
ResourceId 6071
ShotEffectId 538

// logic:
Damage 98
BestRange 125.0
StanceFactor 0 2.1
StanceFactor 1 2.9
StanceFactor 2 2.65
StanceFactor 3 2.8
Burst 3
Auto 30
RPM 9625
ClipSize 30
//GunType AssaultRifle
//Ammunition 50cal
//Quality 9850
}
"""

testString3 = """
// SCAR-L Urban
Weapon (70, Rifle)
{
Weight 400
Price 400
ResourceId 6071
ShotEffectId 538

// logic:
Damage 98
BestRange 125.0
StanceFactor 0 2.1
StanceFactor 1 2.9
StanceFactor 2 2.65
StanceFactor 3 2.8
Burst 3
Auto 30
RPM 9625
ClipSize 30
GunType AssaultRifle
Ammunition 50cal
Quality 9850

Icon 0 448 800 112 40
Picture 8 3 4 3

AnchorPoint 0.0 1.1 0.25

Deliverable

}
"""
pprint.pprint( classDef.parseString(testString) )

#filename = "weapons.txt"
#f = open(filename)
#text = f.read()
#classDef.parseString(text)


