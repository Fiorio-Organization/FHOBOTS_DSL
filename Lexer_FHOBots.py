#Gabriel Acacio Sciamana RA:109006
#Victor Fiorio Casarin   RA:110332
#Vinícius Fiorio Casarin RA:110078

#from ply import lex
import lex as lex
import sys

tokens = (
    "ONENTRY","ONSTATE","ONEXIT","TRANSITION", "STATE_DECLARATION", "ROBOT", "WORLDMODEL",
    "ARITHMETIC_OPERATOR", "ASSIGNMENT_OPERATOR", "ROLE_DECLARATION",
    "STATE_TRANSITION", "OPEN_BRACKET", "CLOSE_BRACKET",
    "OPEN_PARENTHESIS", "CLOSE_PARENTHESIS", "SEPARATOR", "IDENTIFIER",
    "VARIABLE_DECLARATION", "BOOL", "FLOAT_DOUBLE", "INT", "CHAR", "STRING", 
    "IF","ELIF", "ELSE", "END_IF", "COLON", "COMPARISON_OPERATOR"
)

t_ONSTATE = "\@"
t_ARITHMETIC_OPERATOR = "\+|\-|\*|\/|\%" 
t_ASSIGNMENT_OPERATOR = "\="
t_COMPARISON_OPERATOR = "\=\=|\!\=|\<\=|\>\=|\<|\>"
t_OPEN_BRACKET = "\["
t_CLOSE_BRACKET = "\]"
t_OPEN_PARENTHESIS = "\("
t_CLOSE_PARENTHESIS = "\)"
t_SEPARATOR = "\,"
t_IDENTIFIER = "[A-Za-z]\w*"
t_FLOAT_DOUBLE = "\d+\.\d+"
t_CHAR = "\'[A-Za-z0-9]\'"
t_STRING = "\"\w*\""

def t_NEXT_LINE(t):
    r"\n"
    t.lexer.lineno += 1
# Esses tokens são pré-definidos e não precisam comparecer na tupla "tokens"
t_ignore = " "

def t_error(t):
    print(t, "Not recognized!")
    sys.exit(1)

def t_VARIABLE_DECLARATION(t):
    "int|float|char|double|bool"
    return t    

def t_STATE_DECLARATION(t):
    "State:"
    return t

def t_ROLE_DECLARATION(t):
    "Role:"
    return t

def t_ROBOT(t):
    "r\."
    return t

def t_WORLDMODEL(t):
    "world\."
    return t

def t_STATE_TRANSITION(t):
    "\$"
    return t

def t_IF(t):
    "if\s"
    return t

def t_ELSE_IF(t):
    "else\s+if\s"
    return t

def t_ELSE(t):
    "else"
    return t

def t_END_IF(t):
    "endif\s"
    return t

def t_COLON(t):
    ":"
    return t

# garantindo ordem de prioridade / 
# evitando conflito com t_operador_aritmetico
def t_ONENTRY(t):
    "\-\>"
    return t

def t_ONEXIT(t):
    "\<\-"
    return t

def t_TRANSITION(t):
    "\<\>"
    return t

def t_BOOL(t) :
    "true|false"
    return t

def t_INT(t):
    "\d+"
    return t

def initializeLexer(file):
    # Terceiro passo: abrir o código fonte
    file = open(file)
    content = file.read()

    #Quarto passo: instanciar o lexer e carregar o conteúdo
    l = lex.lex()
    l.input(content)
    return l

def nextToken():
    return l.token() #lê o proximo token

file = open('estados_teste.txt')
content = file.read()
print()

l = lex.lex()
l.input(content)

while True:
    t = l.token() 
    if not t:
        break
    print(t)