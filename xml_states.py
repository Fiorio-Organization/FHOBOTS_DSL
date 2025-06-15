import re
import xml.etree.ElementTree as ET
from collections import defaultdict

# Caminho do arquivo stateFactory.hpp
STATE_FACTORY_PATH = "machinestate/header/stateFactory.hpp"
OUTPUT_XML = "states.xml"

# Regex para capturar includes do tipo: #include "folder/stateName.hpp"
INCLUDE_REGEX = re.compile(r'#include\s+"([\w]+)/([\w]+)\.hpp"')

def extrair_estados_com_categorias(caminho_arquivo):
    """
    Retorna um dicionário no formato:
    {
        'goalkeeper': ['seekBallGK', 'spinGK'],
        'common': ['gotoPoint'],
        ...
    }
    """
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        return {}

    categorias = defaultdict(list)
    for pasta, estado in INCLUDE_REGEX.findall(conteudo):
        categorias[pasta].append(estado)
    
    return categorias

def formatar_nome_com_sublinhado_maiusculo(nome_str):
    """
    Formata uma string capitalizando a primeira letra e qualquer letra
    que venha após um sublinhado '_', mantendo o caso original do restante.
    Ex: "attackerCentral" -> "AttackerCentral"
    Ex: "DFC_clearSideBall" -> "DFC_ClearSideBall"
    """
    if not nome_str:
        return ""

    formatted_parts = []
    
    # Capitaliza o primeiro caractere da string se for alfabético
    if nome_str[0].isalpha():
        formatted_parts.append(nome_str[0].upper())
    else:
        formatted_parts.append(nome_str[0])

    # Itera a partir do segundo caractere para aplicar a regra do sublinhado
    for i in range(1, len(nome_str)):
        char = nome_str[i]
        prev_char = nome_str[i-1]

        # Se o caractere anterior for um sublinhado, capitaliza o caractere atual
        if prev_char == '_':
            formatted_parts.append(char.upper())
        else:
            formatted_parts.append(char)
    
    return "".join(formatted_parts)

def gerar_xml_organizado_por_categoria(estados_por_categoria, arquivo_saida):
    root = ET.Element("states")

    for categoria, estados in sorted(estados_por_categoria.items()):
        categoria_formatada = categoria[0].upper() + categoria[1:]
        categoria_elem = ET.SubElement(root, "category", name=categoria_formatada)
        for estado in sorted(estados):
            estado_formatado = formatar_nome_com_sublinhado_maiusculo(estado)
            ET.SubElement(categoria_elem, "state", name=estado_formatado)
    
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)  # Python 3.9+
    tree.write(arquivo_saida, encoding="utf-8", xml_declaration=True)
    print(f"XML gerado com sucesso: {arquivo_saida}")

# Execução
if __name__ == "__main__":
    estados_por_categoria = extrair_estados_com_categorias(STATE_FACTORY_PATH)
    gerar_xml_organizado_por_categoria(estados_por_categoria, OUTPUT_XML)
