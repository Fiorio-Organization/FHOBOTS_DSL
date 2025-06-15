import xml.etree.ElementTree as ET
import re

# Arquivos de entrada e saída
XML_PATH = "states.xml"
HPP_PATH = "model/header/robot.hpp"

def extrair_metodos_robot(caminho_arquivo):
    metodos = []
    # Assume métodos declarados como: void moveTo(...);
    padrao = re.compile(r'\b(?:void|int|float|double|bool|std::string)\s+(\w+)\s*\([^;]*\)\s*;')

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if linha.startswith("//") or not linha or "class " in linha:
                continue
            match = padrao.search(linha)
            if match:
                metodos.append(match.group(1))
    return metodos

def adicionar_categoria_metodos(xml_path, metodos_robot):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Encontra ou cria o nó <robot>
    robot_elem = root.find("robot")
    if robot_elem is None:
        robot_elem = ET.SubElement(root, "robot")

    # Cria nova categoria para métodos
    categoria = ET.SubElement(robot_elem, "category", name="robotMethods")

    for metodo in sorted(metodos_robot):
        ET.SubElement(categoria, "Method", name=metodo)

    ET.indent(tree, space="  ", level=0)
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)
    print(f"Categoria <robotMethods> adicionada ao XML: {xml_path}")

if __name__ == "__main__":
    metodos = extrair_metodos_robot(HPP_PATH)
    adicionar_categoria_metodos(XML_PATH, metodos)
