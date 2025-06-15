import xml.etree.ElementTree as ET
import re

# Arquivos de entrada e saída
XML_INPUT = "states.xml"
HPP_INPUT = "model/header/robot.hpp"
XML_OUTPUT = "states.xml"  # sobrescreve o original

def extrair_atributos_robot(caminho_arquivo):
    atributos = []
    padrao = re.compile(r'\b(?:std::)?\w+\s+(\w+)\s*;')  # Ex: std::string nome;
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if linha.startswith("//") or not linha or '(' in linha or ')' in linha:
                continue
            match = padrao.search(linha)
            if match:
                atributos.append(match.group(1))
    return atributos

def adicionar_categoria_robot(xml_path, atributos_robot):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Cria um novo root que engloba <states> e <robot>
    novo_root = ET.Element("root")
    novo_root.append(root)  # Adiciona <states>

    # Cria e adiciona <robot> como irmão
    robot_elem = ET.SubElement(novo_root, "robot")
    categoria = ET.SubElement(robot_elem, "category", name="robotAttributes")

    for attr in sorted(atributos_robot):
        ET.SubElement(categoria, "Attribute", name=attr)

    tree = ET.ElementTree(novo_root)
    ET.indent(tree, space="  ", level=0)
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)
    print(f"Seção <robot> adicionada ao XML como elemento externo a <states>: {xml_path}")

if __name__ == "__main__":
    atributos = extrair_atributos_robot(HPP_INPUT)
    adicionar_categoria_robot(XML_INPUT, atributos)
