
# es
kb = """
1234567890-=
qwertyuiop´`
asdfghjklñ;'
<zxcvbnm,.ç
"""

kb_shift = """
¡!#$%/&*()_+
QWERTYUIOPº¨
ASDFGHJKLÑ:"
>ZXCVBNM¿?Ç
"""

# fr
kb = """
&é"'(§è!çà)-
azertyuiop^$
qsdfghjklmù`
<wxcvbn,;:=
"""

kb_shift = """
1234567890°_
AZERTYUIOP¨*
QSDFGHJKLM%£
>WXCVBN?./+
"""


# it
kb = """
1234567890'ì
qwertyuiopè+
asdfghjklòàù
<zxcvbnm,.-
"""

kb_shift = """
!"£$%&/()=?^
QWERTYUIOPé*
ASDFGHJKLç°§
>ZXCVBNM;:_
"""


# lt
kb = """
ąčęėįšųū90-ž
qwertyuiop[]
asdfghjkl;'\\
`zxcvbnm,./
"""

kb_shift = """
ĄČĘĖĮŠŲŪ()_Ž
QWERTYUIOP{}
asdfghjkl;'\\
`zxcvbnm,./
"""


# mk
kb = """
1234567890-=
љњертѕуиопшѓ
асдфгхјклчќж
ѝзџцвбнм,./
"""

kb_shift = """
!„“'%‚‘*()_+
ЉЊЕРТSУИОПШЃ
АСДФГХЈКЛЧЌЖ
ЍЗЏЦВБНМ;:?
"""



# nb
kb = """
1234567890+´
qwertyuiopå¨
asdfghjklæø'
<zxcvbnm,.-
"""

kb_shift = """
!"#€%&/()=?`
QWERTYUIOPÅ^
ASDFGHJKLÆØ*
>ZXCVBNM;:_
"""


# nl
kb = """
1234567890-=
qwertyuiop[]
asdfghjkl;'\\
`zxcvbnm,./
"""

kb_shift = """
!@#$%^&*()_+
QWERTYUIOP{}
ASDFGHJKL:"|
~ZXCVBNM<>?
"""


# pl
kb = """
1234567890-=
qwertyuiop[]
asdfghjkl;'\\
`zxcvbnm,./
"""

kb_shift = """
!@#$%^&*()_+
QWERTYUIOP{}
ASDFGHJKL:"|
~ZXCVBNM<>?
"""


# pt
kb = """
1234567890'+
qwertyuiopº´
asdfghjklç~\\
<zxcvbnm,.-
"""

kb_shift = """
!"#$%&/()=?*
QWERTYUIOPª`
ASDFGHJKLÇ^|
>ZXCVBNM;:_
"""


# ro
kb = """
1234567890'+
qwertyuiopº´
asdfghjklç~\\
<zxcvbnm,.-
"""

kb_shift = """
!"#$%&/()=?*
QWERTYUIOPª`
ASDFGHJKLÇ^|
>zxcvbnm,._
"""


# ru
kb = """
1234567890-=
йцукенгшщзхъ
фывапролджэё
]ячсмитьбю/
"""

kb_shift = """
!"№%:,.;()_+
ЙЦУКЕНГШЩЗХЪ
ФЫВАПРОЛДЖЭЁ
[ЯЧСМИТЬБЮ?
"""





[[t for t in r] for r in kb.split("\n") if r]
[[t for t in r] for r in kb_shift.split("\n") if r]


