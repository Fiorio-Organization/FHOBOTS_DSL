#Gabriel Acacio Sciamana RA:109006
#Victor Fiorio Casarin   RA:110332
#Vinícius Fiorio Casarin RA:110078

from Lexer_FHOBots import inicializaLexer
import sys

lexer = inicializaLexer("estados_teste.txt")

# pega o proximo token
lookAhead = lexer.token() # Inicialiando o lookAhead

# roles e estados declarados na Máquina de Estados
roles_estados_existentes = {
    "Common": ["GotoPoint", "Backoff", "GotoBall"],
    "Goalkeeper": ["SpinGK"],
    "Defender": ["SeekBallDEF"]
}

# class robot
robotMethods = {"move", "setObjective", "setOrientationObjective"}
robotAttributes = {"isStopped", "robotTimer", "x", "y","xObj", "yObj","role"}

# class worldmodel
worldModel_atributos = {}
worldModel_metodos = {}

    ########################
#   Verificar Existencia de Role e Estado  #
    ########################

def verificaExistenciaEstado(estado):
    global roles_estados_existentes
    for roles in roles_estados_existentes.values():
        if estado in roles:
            return True
    return False

def verificaExistenciaRole(lexema):
    global roles_estados_existentes
    return lexema in roles_estados_existentes
    
def verificaExistenciaEstadoTransition(role, estado):
    global roles_estados_existentes
    return estado in roles_estados_existentes[role]

    ########################

#verificando se o token criado é coerente com a gramática
def match(esperado):
    global lookAhead
    if lookAhead != None and esperado == lookAhead.type:
        lookAhead = lexer.token() #continua o processo
        return
    
    # se não, tenho um erro sintático
    print("Erro sintático na linha", lexer.lineno, "Esperado", esperado, "lido", lookAhead)
    sys.exit(1) #1 indica que houve erro

# link_transition > Novo_papel | estado_de_transicao | programa | ϵ
def link_transicao():
    global lookAhead
    if lookAhead != None: # se não é fim de arquivo (ϵ)
        if lookAhead.type == "ROLE_DECLARACAO":
            novo_papel()
        elif lookAhead.type == "ESTADO_TRANSICAO":
            estado_de_transicao()
        elif lookAhead.type == "STATE_DECLARACAO":
            programa()

# estado_de_transição > $#nome_do_estado [condição] [tratativas] link_transition 
def estado_de_transicao():
    match("ESTADO_TRANSICAO")
    match("IDENTIFICADOR")
    match("ABRE_COLCHETE")
    #condicao()
    match("FECHA_COLCHETE")
    match("ABRE_COLCHETE")
    #tratativa()
    match("FECHA_COLCHETE")
    link_transicao()

# Novo_papel > Role: #papel_do_robo estado__de_transição
def novo_papel():
    match("ROLE_DECLARACAO")
    match("IDENTIFICADOR")
    estado_de_transicao()

# transition > <> Novo_papel
def transition():
    match("TRANSITION")
    novo_papel()

def checkRobotAttributes(attribute, line):
    if not attribute in robotAttributes:
        print("Semantic error on line " + str(line) +":",
        "Attribute " + attribute + " doesn't exist")
        sys.exit(1)
    #else:
        #print("Attribute " + attribute + " exists")

def checkRobotAttributesAndMethods():
    match("ROBOT")
    lexema = lookAhead.value
    match("IDENTIFICADOR")
    if lookAhead.type == "OPERADOR_ATRIBUICAO":
        match("OPERADOR_ATRIBUICAO")
        checkRobotAttributes(lexema, lookAhead.lineno)
        tipoDado()
    
    elif lookAhead.type == "ABRE_PARENTESES":
        match("ABRE_PARENTESES")
        if lookAhead.type == "IDENTIFICADOR":
            match("IDENTIFICADOR")
            parametros()
        match("FECHA_PARENTESES")

def corpoOnExit():
    if lookAhead.type != "TRANSITION":
        checkRobotAttributesAndMethods()
        corpoOnExit()

# onExit > <- corpoOnExit
def onExit():
    match("ONEXIT")
    corpoOnExit()

# onState > @ corpoOnState
def onState():
    match("ONSTATE")
    #corpoOnState()
        #if lookAhead.type == "ROBOT"
        #elif lookAhead.type == "WORLDMODEL"
        #elif lookAhead.type == "IF"

# tipoDado > bool | int | float_double | string | char | var
def tipoDado():
    if lookAhead.type == "BOOL":
        match("BOOL")
    elif lookAhead.type == "INT":
        match("INT")
    elif lookAhead.type == "FLOAT_DOUBLE":
        match("STRING")
    elif lookAhead.type == "STRING":
        match("STRING")
    elif lookAhead.type == "CHAR":
        match("CHAR")
    elif lookAhead.type == "IDENTIFICADOR":
        match("IDENTIFICADOR")

# parametros > , #var parametros | ϵ
def parametros():
    if lookAhead.type == "SEPARADOR":
        match("SEPARADOR")
        match("IDENTIFICADOR")


# corpoOnEntry > r.#Var = tipoDado | r.#Var(parametros) | ϵ
def corpoOnEntry():
    if lookAhead.type != "ONSTATE":
        checkRobotAttributesAndMethods()
        corpoOnEntry()

# onEntry > -> corpoOnEntry
def onEntry():
    match("ONENTRY")
    corpoOnEntry()

# Programa > State: #Nome_do_Estado onEntry onState onExit transition
def programa():
    match("STATE_DECLARACAO")
    match("IDENTIFICADOR")
    onEntry()
    onState()
    onExit()
    transition()

print("--------")
programa()
print("Sintaticamente correto!")