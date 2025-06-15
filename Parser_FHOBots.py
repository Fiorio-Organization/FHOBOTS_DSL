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

# lista com Roles e States
rolesAndStates ={"roles": list(rolesAndStatesFromStateMachine.keys()),
                 "states": [state for states in rolesAndStatesFromStateMachine.values() for state in states]}

# class robot
robotMethods = {"move", "stop", "setObjective", "setOrientationObjective"}
robotAttributes = {"isStopped", "robotTimer", "x", "y","xObj", "yObj","role"}

# class worldModel
worldModelAttributes = {"isPlayingLeft"}
worldModelMethods = {"isStuck"}

# declared vars
declaredVars = {}

    ########################
#   Verificar Existencia de Role e Estado  #
    ########################

def stateExists(state):
    global rolesAndStatesFromStateMachine
    for roles in rolesAndStatesFromStateMachine.values():
        if state in roles:
            return True
    return False

def roleExists(lexeme):
    global rolesAndStatesFromStateMachine
    return lexeme in rolesAndStatesFromStateMachine
    
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
def link_transition():
    global lookAhead
    if lookAhead != None: # se não é fim de arquivo (ϵ)
        if lookAhead.type == "ROLE_DECLARATION":
            new_role()
        elif lookAhead.type == "STATE_TRANSITION":
            transition_state()
        

# estado_de_transição > $#nome_do_estado [condição] [tratativas] link_transition 
def transition_state():
    match("STATE_TRANSITION")
    id_state = lookAhead.value
    match("IDENTIFIER")
    match("OPEN_BRACKET")
    if lookAhead.type != "CLOSE_BRACKET":
        cpp_file.write(
            f"\tif("
        )
        checkComparison()
        cpp_file.write(
            f"){{\n"
        )
    match("CLOSE_BRACKET")
    match("OPEN_BRACKET")
    if lookAhead.type != "CLOSE_BRACKET":
        Body()
    match("CLOSE_BRACKET")

    cpp_file.write(
        f"\treturn StateFactory::getInstance(\"{id_state}\");\n"
    )

    cpp_file.write(
        f"}}\n"
    )
    link_transition()

# Novo_papel > Role: #papel_do_robo estado_de_transição
def new_role():
    global id_role
    global id_state
    global cpp_file
    match("ROLE_DECLARATION")
    id_role = lookAhead.value
    if not roleExists(id_role):
        print("Semantic error on line " + str(lookAhead.lineno) +":",
        "Role " + id_role + " not declared in state " + id_state)
        sys.exit(1)
    
    if not id_role == "Common":
        cpp_file.write(
            f"\nif(robot->role == {id_role}Role::getInstance()) {{\n"
        )
    
    match("IDENTIFIER")
    transition_state()
    if not id_role == "Common":
        cpp_file.write(
            f"}}\n"
        )

# transition > <> Novo_papel
def transition():
    match("TRANSITION")
    cpp_file.write(
        f"void {id_state}::transition(Robot * robot, IWorldModel * worldModel){{\n"
    )
    new_role()
    '''cpp_file.write(
        f"}}\n\n"
    )'''

# parametros > , #var parametros | ϵ
def parameters():
    m = lookAhead.value
    dataType()
    if lookAhead.type == "SEPARATOR":
        match("SEPARATOR")
        parameters()

def checkIdentifier():
    global id_state
    global cpp_file
    lexeme = lookAhead.value
    match("IDENTIFIER")
    if not lexeme in declaredVars:
        print("Semantic error on line " + str(lookAhead.lineno) +":",
        "Identifier " + lexeme + " not declared in state " + id_state)
        sys.exit(1)
    cpp_file.write(
        f"\t{lexeme}"
    )
    if lookAhead.type == "ASSIGNMENT_OPERATOR":
        match("ASSIGNMENT_OPERATOR")
        td = lookAhead.value
        dataType()
        cpp_file.write(
            f" = {td};\n"
        )
    
    else:
        print("Semantic error on line " + str(lookAhead.lineno) +":",
        "Identifier " + lexeme + " not assigned in state " + id_state)

def checkVarDeclaration():
    global id_state
    global cpp_file
    variableType = lookAhead.value
    match("VARIABLE_DECLARATION")
    lexema = lookAhead.value
    match("IDENTIFIER")
    
    if lexema in declaredVars:
        print("Semantic error on line " + str(lookAhead.lineno) +":",
        "Variable " + lexema + " already declared in state " + id_state)
        sys.exit(1)
    
    declaredVars[lexema] = True
    
    cpp_file.write(
        f"\t{variableType} {lexema}"
    )
    
    if lookAhead.type == "ASSIGNMENT_OPERATOR":
        match("ASSIGNMENT_OPERATOR")
        td = lookAhead.value
        dataType()
        cpp_file.write(
            f" = {td}"
        )
    cpp_file.write(
            f";\n"
        )

def checkWorldModelAttributes(attribute, line):
    if not attribute in worldModelAttributes:
        print("Semantic error on line " + str(line) +":",
        "Attribute " + attribute + " doesn't exist in WorldModel")
        sys.exit(1)

def checkWorldModelMethods(method, line):
    if not method in worldModelMethods:
        print("Semantic error on line " + str(line) +":",
        "Method " + method + " doesn't exist in WorldModel")
        sys.exit(1)

def checkWorldModel():
    global id_state
    global cpp_file
    match("WORLDMODEL")
    lexema = lookAhead.value
    match("IDENTIFIER")
    cpp_file.write(
        f"worldModelVss->{lexema}"
    )
    if lookAhead.type == "ASSIGNMENT_OPERATOR":
        match("ASSIGNMENT_OPERATOR")
        td = lookAhead.value
        checkWorldModelAttributes(lexema, lookAhead.lineno)
        dataType()
        cpp_file.write(
            f" = {td}"
        )
    elif lookAhead.type == "OPEN_PARENTHESIS":
        match("OPEN_PARENTHESIS")
        cpp_file.write(
            f"("
        )
        
        checkWorldModelMethods(lexema, lookAhead.lineno)            
        parameters()
        match("CLOSE_PARENTHESIS")
        cpp_file.write(
            f")"
        )

def checkRobotAttributes(attribute, line):
    if not attribute in robotAttributes:
        print("Semantic error on line " + str(line) +":",
        "Attribute " + attribute + " doesn't exist")
        sys.exit(1)

def checkRobotMethods(method, line):
    if not method in robotMethods:
        print("Semantic error on line " + str(line) +":",
        "Method " + method + " doesn't exist")
        sys.exit(1)

def checkRobot():
    global id_state
    global cpp_file
    match("ROBOT")
    lexeme = lookAhead.value
    match("IDENTIFIER")
    cpp_file.write(
        f"robot->{lexeme}"
    )
    if lookAhead.type == "ASSIGNMENT_OPERATOR":
        match("ASSIGNMENT_OPERATOR")
        td = lookAhead.value
        checkRobotAttributes(lexeme, lookAhead.lineno)
        dataType()
        cpp_file.write(
            f" = {td}"
        )
    
    elif lookAhead.type == "OPEN_PARENTHESIS":
        match("OPEN_PARENTHESIS")
        cpp_file.write(
            f"("
        )
        
        checkRobotMethods(lexeme, lookAhead.lineno)            
        parameters()
        match("CLOSE_PARENTHESIS")
        cpp_file.write(
            f")"
        )

# onExit > <- corpoOnExit
def onExit():
    global id_state
    global cpp_file
    match("ONEXIT")
    cpp_file.write(
        f"void {id_state}::onExit(Robot * robot, IWorldModel * worldModel){{\n"
    )
    Body()
    cpp_file.write(
        f"}}\n\n"
    )

# onState > @ corpoOnState
def onState():
    global id_state
    global cpp_file
    match("ONSTATE")
    cpp_file.write(
        f"void {id_state}::onState(Robot * robot, IWorldModel * worldModel){{\n"
    )
    Body()
    cpp_file.write(
        f"}}\n\n"
    )

# tipoDado > bool | int | float_double | string | char | var
def dataType():
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
        checkRobot()
    elif lookAhead.type == "WORLDMODEL": # world.attribute
        checkWorldModel()

def checkIfChaining():
    if lookAhead.type == "IF_SEP":
        cpp_file.write(
            f" {lookAhead.value} "
        )
        match("IF_SEP")
        checkComparison()

def checkComparison():
    if lookAhead.type == "OPEN_PARENTHESIS":
        match("OPEN_PARENTHESIS")
        cpp_file.write(
            f"("
        )
        checkComparison()
        match("CLOSE_PARENTHESIS")
        cpp_file.write(
            f")"
        )
    else:
        if lookAhead.type == "IDENTIFIER" or lookAhead.type == "ROBOT" or lookAhead.type == "WORLDMODEL" or lookAhead.type == "BOOL" or lookAhead.type == "INT" or lookAhead.type == "FLOAT_DOUBLE" or lookAhead.type == "STRING" or lookAhead.type == "CHAR" :
            cpp_file.write(
                f"{lookAhead.value}"
            )
        dataType()
        if lookAhead.type == "COMPARISON_OPERATOR":
            cpp_file.write(
                f" {lookAhead.value} "
            )
        match("COMPARISON_OPERATOR")
        if lookAhead.type == "IDENTIFIER" or lookAhead.type == "ROBOT" or lookAhead.type == "WORLDMODEL" or lookAhead.type == "BOOL" or lookAhead.type == "INT" or lookAhead.type == "FLOAT_DOUBLE" or lookAhead.type == "STRING" or lookAhead.type == "CHAR" :
            cpp_file.write(
                f"{lookAhead.value}"
            )
        dataType()
    checkIfChaining()

def checkComparisonStatement():
    match("IF")
    global cpp_file
    cpp_file.write(
        f"\tif("
    )
    checkComparison()
    match("OPEN_CURLY_BRACE")
    cpp_file.write(
        f"){{\n"
    )

    Body()
    
    match("CLOSE_CURLY_BRACE")
    cpp_file.write(
        f"\n\t}}\n"
    )

    if lookAhead.type == "ELSE_IF":
        match("ELSE_IF")
        cpp_file.write(
            f"\telse if("
        )
        checkComparison()
        match("OPEN_CURLY_BRACE")
        cpp_file.write(
            f"){{\n"
        )
        Body()

        match("CLOSE_CURLY_BRACE")
        cpp_file.write(
            f"\n\t}}\n"
        )

    elif lookAhead.type == "ELSE":
        match("ELSE")
        cpp_file.write(
            f"\telse"
        )
        match("OPEN_CURLY_BRACE")
        cpp_file.write(
            f"{{\n"
        )
        Body()

        match("CLOSE_CURLY_BRACE")
        cpp_file.write(
            f"\n\t}}\n"
        )

def checkBody():
    if lookAhead.type == "ROBOT":
        checkRobot()
    elif lookAhead.type == "WORLDMODEL":
        checkWorldModel()
    elif lookAhead.type == "VARIABLE_DECLARATION":
        checkVarDeclaration()
    elif lookAhead.type == "IDENTIFIER":
        checkIdentifier()
    elif lookAhead.type == "IF":
        checkComparisonStatement()

# corpoOnEntry > r.#Var = tipoDado | r.#Var(parametros) | ϵ
def Body():
    look = lookAhead.type
    if (lookAhead.type == "ROBOT" or lookAhead.type == "WORLDMODEL" or 
        lookAhead.type == "VARIABLE_DECLARATION" or lookAhead.type == "IDENTIFIER" or
        lookAhead.type == "IF"):
        if look == "ROBOT" or look == "WORLDMODEL":
            cpp_file.write(
                f"\t"
            )   
        checkBody()
        if look == "ROBOT" or look == "WORLDMODEL":
            cpp_file.write(
                f";\n"
            )
        Body()

# onEntry > -> corpoOnEntry
def onEntry():
    global id_state
    global cpp_file
    match("ONENTRY")
    cpp_file.write(
        f"void {id_state}::onEntry(Robot * robot, IWorldModel * worldModel){{\n"
    )
    Body()
    cpp_file.write(
        f"}}\n\n"
    )

# Programa > State: #Nome_do_Estado onEntry onState onExit transition
def program():
    global id_role
    id_role = lookAhead.value
    id_role_name = id_role[0].lower() + id_role[1:]

    match("STATE_DECLARATION")

    global id_state
    id_state = lookAhead.value

    id_state_name = id_state[0].lower() + id_state[1:]
    
    id_state_header = ""
    for char in id_state_name:
        if char.isupper():
            id_state_header += "_"
        id_state_header += char
    id_state_header = id_state_header.upper()

    match("IDENTIFIER")

    global hpp_file
    # Garante que o diretório exista
    os.makedirs("header", exist_ok=True)
    hpp_file = open("header/" + id_state_name + ".hpp", "w")
    hpp_file.write(
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

    global cpp_file
    os.makedirs("src", exist_ok=True)
    cpp_file = open("src/" + id_state_name + ".cpp", "w")
    cpp_file.write(
        f"#include \"../../header/common/{id_state_name}.hpp\"\n"
        f"#include <iostream>\n\n"
        f"{id_state} * {id_state}::instance = NULL;\n\n"
        f"{id_state}::{id_state}(std::string stateLabel){{\n"
        f"\tthis->stateLabel = stateLabel;\n"
        f"}}\n\n"
    )
    
    onEntry()
    onState()
    onExit()
    transition()
    
    cpp_file.write(
        f"{id_state} * {id_state}::getInstance(std::string stateLabel){{\n"
        f"\tif({id_state}::instance == NULL)\n"
        f"\t\t{id_state}::instance = new {id_state}(stateLabel);\n\n"
        f"\treturn {id_state}::instance;\n"
        f"}}"
    )

    if lookAhead != None:
        if lookAhead.type == "STATE_DECLARATION":
            program()

print("--------")
program()
print("Syntactically correct!")

    #############
    #   DEBUG   #
    #############

# Debug functions
def printDeclaredVars():
    print("Declared Variables:")
    for var in declaredVars:
        print(f"- {var}")

def printRolesAndStates():
    print("Roles and States:")
    for role, states in rolesAndStatesFromStateMachine.items():
        print(f"Role: {role}")
        for state in states:
            print(f"  - State: {state}")

def printRolesAndStatesList():
    print("Roles and States List:")
    for role in rolesAndStates["roles"]:
        print(f"Role: {role}")
        for state in rolesAndStatesFromStateMachine[role]:
            print(f"  - State: {state}")

print("--------")
print("DEBUG\n")
#printDeclaredVars()
#printRolesAndStates()
printRolesAndStatesList()