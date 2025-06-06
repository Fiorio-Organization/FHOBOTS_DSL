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

def gerar_xml_organizado_por_categoria(estados_por_categoria, arquivo_saida):
    root = ET.Element("states")

    for categoria, estados in sorted(estados_por_categoria.items()):
        categoria_elem = ET.SubElement(root, "category", name=categoria)
        for estado in sorted(estados):
            ET.SubElement(categoria_elem, "state", name=estado)
    
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)  # Python 3.9+
    tree.write(arquivo_saida, encoding="utf-8", xml_declaration=True)
    print(f"XML gerado com sucesso: {arquivo_saida}")

# Execução
if __name__ == "__main__":
    estados_por_categoria = extrair_estados_com_categorias(STATE_FACTORY_PATH)
    gerar_xml_organizado_por_categoria(estados_por_categoria, OUTPUT_XML)
