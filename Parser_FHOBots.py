#Gabriel Acacio Sciamana RA:109006
#Victor Fiorio Casarin   RA:110332
#Vinícius Fiorio Casarin RA:110078

from Lexer_FHOBots import initializeLexer
import sys
import xml.etree.ElementTree as ET # xml
import os # pasta de arquivos

lexer = initializeLexer("estados_teste.txt")

# pega o proximo token
lookAhead = lexer.token() # Inicialiando o lookAhead

# roles e estados declarados na Máquina de Estados
def loadRolesAndStatesFromXML(xml_file):
    roles_states = {} # dicionario de roles e states
    tree = ET.parse(xml_file) # tree recebe estrutura xml
    root = tree.getroot() # obtem raiz State
    # obtendo todos os name de states em cada category do arquivo xml
    for category in root.findall('category'):
        role_name = category.get('name')
        # encontra e associa um state a uma role (chave)
        states = [state.get('name') for state in category.findall('state')] # states.append(state.get('name'))
        roles_states[role_name] = states 
    return roles_states

rolesAndStatesFromStateMachine = loadRolesAndStatesFromXML("states.xml")
#print(rolesAndStatesFromStateMachine)

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
    global id_state
    global arquivo_cpp
    match("ROBOT")
    lexema = lookAhead.value
    match("IDENTIFIER")
    arquivo_cpp.write(
    f"robot->{lexema} "
    )
    if lookAhead.type == "ASSIGNMENT_OPERATOR":
        match("ASSIGNMENT_OPERATOR")
        td = lookAhead.value
        checkRobotAttributes(lexema, lookAhead.lineno)
        tipoDado()
        arquivo_cpp.write(
        f"= {td}\n"
        )
    
    elif lookAhead.type == "OPEN_PARENTHESIS":
        match("OPEN_PARENTHESIS")
        m = lookAhead.value
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
    global id_state
    global arquivo_cpp
    match("ONENTRY")
    arquivo_cpp.write(
f"void {id_state}::onEntry(Robot * robot, IWorldModel * worldModel){{\n"
)
    corpoOnEntry()

# Programa > State: #Nome_do_Estado onEntry onState onExit transition
def programa():
    global id_role
    id_role = lookAhead.value
    id_role_name = id_role[0].lower() + id_role[1:]

    match("STATE_DECLARATION")

    global id_state
    id_state = lookAhead.value
    id_state_name = id_state[0].lower() + id_state[1:]
    id_state_header = id_state.upper()

    match("IDENTIFIER")

    global arquivo_hpp
    # Garante que o diretório exista
    os.makedirs("header", exist_ok=True)
    arquivo_hpp = open("header/" + id_state_name + ".hpp", "w")
    arquivo_hpp.write(
f"#ifndef {id_state_header}_HPP\n"
f"#define {id_state_header}_HPP\n\n"
f"class {id_state}: public State{{\n"
f"private:\n"
f"    {id_state}(std::string stateLabel);\n\n"
f"public:\n" 
f"    void onEntry(Robot * robot, IWorldModel * worldModel);\n"
f"    void onState(Robot * robot, IWorldModel * worldModel);\n"
f"    void onExit (Robot * robot, IWorldModel * worldModel);\n"
f"    State * transition(Robot * robot, IWorldModel * worldModel);\n"
f"    static {id_state} * getInstance(std::string stateLabel);\n"
f"    static {id_state} * instance;\n"
f"}};\n\n"
f"#endif"
    )

    global arquivo_cpp
    os.makedirs("src", exist_ok=True)
    arquivo_cpp = open("src/" + id_state_name + ".cpp", "w")
    arquivo_cpp.write(
f"#include \"../../header/common/{id_state_name}.hpp\"\n"
f"#include <iostream>\n\n"
f"{id_state} * {id_state}::instance = NULL;\n\n"
f"{id_state}::{id_state}(std::string stateLabel){{\n"
f"    this->stateLabel = stateLabel;\n"
f"}}\n\n"
    )

    onEntry()
    onState()
    onExit()
    transition()

print("--------")
programa()
print("Sintaticamente correto!")