#Gabriel Acacio Sciamana RA:109006
#Victor Fiorio Casarin   RA:110332
#Vinícius Fiorio Casarin RA:110078

#from ply import lex
import ply.lex as lex
import sys

tokens = (
    "ONENTRY","ONSTATE","ONEXIT","TRANSITION", "STATE", "ROBOT",
    "OPERADOR_ARITMETICO", "OPERADOR_ATRIBUICAO", "ROLE",
    "ESTADO_TRANSICAO", "ABRE_COLCHETE", "FECHA_COLCHETE",
    "ABRE_PARENTESES", "FECHA_PARENTESES", "SEPARADOR", "VAR",
    "BOOL", "FLOAT_DOUBLE", "INT", "CHAR", "STRING"
)

#t_ONENTRY = r"\-\>" #feito em funcao, prioridade
t_ONSTATE = "\@"
t_ONEXIT = "\<\-"
t_TRANSITION = "\<\>"
t_STATE = "State\:\s[A-Z][A-Za-z]*" # State: Nome_do_Estado
t_ROBOT = "r.[A-Za-z]+" # r.atributo OU r.metodo
t_OPERADOR_ARITMETICO = "\+|\-|\*|\/|\%" 
t_OPERADOR_ATRIBUICAO = "\="
t_ROLE = "Role\:\s[A-Z]\w*"
t_ESTADO_TRANSICAO = "\$[A-Z]\w*\s"
t_ABRE_COLCHETE = "\["
t_FECHA_COLCHETE = "\]"
t_ABRE_PARENTESES = "\("
t_FECHA_PARENTESES = "\)"
t_SEPARADOR = "\,"
t_VAR = "[A-Za-z]\w*"
t_FLOAT_DOUBLE = "\d+\.\d+"
t_CHAR = "[A-Za-z0-9]"
t_STRING = "\"\w*\""

def t_MUDA_LINHA(t):
    r"\n"
    t.lexer.lineno += 1
# Esses tokens são pré-definidos e não precisam comparecer na tupla "tokens"
t_ignore = " "

def t_error(t):
    print(t, "Não foi reconhecido!")
    sys.exit(1)

# garantindo ordem de prioridade / 
# evitando conflito com t_operador_aritmetico
def t_ONENTRY(t):
    "\-\>"
    return t

def t_BOOL(t) :
    "True|False"
    return t

def t_INT(t):
    "\d+"
    return t

def inicializaLexer(arquivo):
    # Terceiro passo: abrir o código fonte
    arquivo = open(arquivo)
    conteudo = arquivo.read()

    #Quarto passo: instanciar o lexer e carregar o conteúdo
    l = lex.lex()
    l.input(conteudo)
    return l

def proximoToken():
    return l.token() #lê o proximo token

arquivo = open('estados_teste.txt')
conteudo = arquivo.read()
print()

l = lex.lex()
l.input(conteudo)

while True:
    t = l.token() 
    if not t:
        break
    print(t)