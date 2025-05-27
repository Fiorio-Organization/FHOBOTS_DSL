#Gabriel Acacio Sciamana RA:109006
#Victor Fiorio Casarin   RA:110332
#Vinícius Fiorio Casarin RA:110078

from Lexer_FHOBots import initializeLexer
import sys

lexer = initializeLexer("estados_teste.txt")

# pega o proximo token
lookAhead = lexer.token() # Inicialiando o lookAhead

# roles e estados declarados na Máquina de Estados
rolesAndStatesFromStateMachine = {
    "Common": ["GotoPoint", "Backoff", "GotoBall"],
    "Goalkeeper": ["SpinGK"],
    "Defender": ["SeekBallDEF"]
}

# class robot
robotMethods = {"move", "stop", "setObjective", "setOrientationObjective"}
robotAttributes = {"isStopped", "robotTimer", "x", "y","xObj", "yObj","role"}

# class worldModel
worldModelAttributes = {}
worldModelMethods = {}

    ########################
#   Verificar Existencia de Role e Estado  #
    ########################

def stateExists(state):
    global rolesAndStatesFromStateMachine
    for roles in rolesAndStatesFromStateMachine.values():
        if state in roles:
            return True
    return False

def roleExists(lexema):
    global rolesAndStatesFromStateMachine
    return lexema in rolesAndStatesFromStateMachine
    
def transitionStateExists(role, state):
    global rolesAndStatesFromStateMachine
    return state in rolesAndStatesFromStateMachine[role]

    ########################

#verificando se o token criado é coerente com a gramática
def match(expected):
    global lookAhead
    if lookAhead != None and expected == lookAhead.type:
        lookAhead = lexer.token() #continua o processo
        return
    
    # se não, tenho um erro sintático
    print("Syntax error on line", lexer.lineno, "Expected", expected, "read", lookAhead)
    sys.exit(1) #1 indica que houve erro

# link_transition > Novo_papel | estado_de_transicao | programa | ϵ
def link_transicao():
    global lookAhead
    if lookAhead != None: # se não é fim de arquivo (ϵ)
        if lookAhead.type == "ROLE_DECLARATION":
            novo_papel()
        elif lookAhead.type == "STATE_TRANSITION":
            estado_de_transicao()
        elif lookAhead.type == "STATE_DECLARATION":
            programa()

# estado_de_transição > $#nome_do_estado [condição] [tratativas] link_transition 
def estado_de_transicao():
    match("STATE_TRANSITION")
    match("IDENTIFIER")
    match("OPEN_BRACKET")
    #condicao()
    match("CLOSE_BRACKET")
    match("OPEN_BRACKET")
    #tratativa()
    match("CLOSE_BRACKET")
    link_transicao()

# Novo_papel > Role: #papel_do_robo estado__de_transição
def novo_papel():
    match("ROLE_DECLARATION")
    match("IDENTIFIER")
    estado_de_transicao()

# transition > <> Novo_papel
def transition():
    match("TRANSITION")
    novo_papel()

# parametros > , #var parametros | ϵ
def parametros():
    tipoDado()
    if lookAhead.type == "SEPARATOR":
        match("SEPARATOR")
        parametros()

def checkRobotAttributes(attribute, line):
    if not attribute in robotAttributes:
        print("Semantic error on line " + str(line) +":",
        "Attribute " + attribute + " doesn't exist")
        sys.exit(1)
    #else:
        #print("Attribute " + attribute + " exists")

def checkRobotMethods(method, line):
    if not method in robotMethods:
        print("Semantic error on line " + str(line) +":",
        "Method " + method + " doesn't exist")
        sys.exit(1)
    #else:
        #print("Method " + attribute + " exists")

def checkRobotAttributesAndMethods():
    match("ROBOT")
    lexema = lookAhead.value
    match("IDENTIFIER")
    if lookAhead.type == "ASSIGNMENT_OPERATOR":
        match("ASSIGNMENT_OPERATOR")
        checkRobotAttributes(lexema, lookAhead.lineno)
        tipoDado()
    
    elif lookAhead.type == "OPEN_PARENTHESIS":
        match("OPEN_PARENTHESIS")
        checkRobotMethods(lexema, lookAhead.lineno)
        parametros()
        match("CLOSE_PARENTHESIS")

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
        match("FLOAT_DOUBLE")
    elif lookAhead.type == "STRING":
        match("STRING")
    elif lookAhead.type == "CHAR":
        match("CHAR")
    elif lookAhead.type == "IDENTIFIER":
        match("IDENTIFIER")
    elif lookAhead.type == "ROBOT": # r.attribute
        match("ROBOT")
        match("IDENTIFIER")

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
    match("STATE_DECLARATION")
    match("IDENTIFIER")
    onEntry()
    onState()
    onExit()
    transition()

print("--------")
programa()
print("Sintaticamente correto!")