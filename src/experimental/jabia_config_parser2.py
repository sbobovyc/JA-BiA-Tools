import pprint
from pyparsing import \
    Keyword,Literal,Word,alphas,nums,alphanums,MatchFirst,OneOrMore,ZeroOrMore,ParserElement,ParseExpression, \
    Group,cppStyleComment,Combine,Optional,Suppress,LineEnd,LineStart,delimitedList,dblQuotedString,restOfLine

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

                   

classKeywords = map(lambda x: Keyword(x), ["Weapon", "Attachment"])
weaponKeywords = map(lambda x: Keyword(x), ["Weight", "Price", "ResourceId",
                                            "ShotEffectId", "Damage", "BestRange",
                                            "StanceFactor", "Burst", "Auto",
                                            "RPM", "ClipSize", "GunType",
                                            "Ammunition", "Quality", "Icon",
                                            "Picture", "DisableAttachments","AnchorPoint",
                                            "Deliverable"
                                            ])
reservedKeywords = MatchFirst(weaponKeywords)
integer = Word(nums)
number = Combine( Optional('-') + ( '0' | Word('123456789',nums) ) +
                    Optional( '.' + integer ) ) 
value = ~reservedKeywords + (number | Word(alphanums) | Word(alphanums + '_' + alphanums))
print nums
print reservedKeywords
statementDef =  Group ( reservedKeywords + Optional( ZeroOrMore(value) ) )
bodyDef = ZeroOrMore( statementDef )
classObj = Group( MatchFirst(classKeywords) + lparan + delimitedList(integer ^ Word(alphas) ^ Combine(Word(alphas) + Literal(" ") + integer) )  + rparan )
classDef =  Group( classObj + lbrace + bodyDef + rbrace )
configFileDef = ZeroOrMore(classDef)
configFileDef.ignore(comment)
configFileDef.ignore(quote)
number.setParseAction( convertNumbers )
integer.setParseAction( convertNumbers )



filename = "weapons.txt"
f = open(filename)
testString = f.read()
#print testString
parsed = configFileDef.parseString(testString)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint( parsed.asList() )





