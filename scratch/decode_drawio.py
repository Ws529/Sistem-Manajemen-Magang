import os
import xml.etree.ElementTree as ET
import base64
import zlib
import urllib.parse
import re

def decode_drawio_diagram(diagram_text):
    try:
        decoded_data = base64.b64decode(diagram_text)
        decompressed_data = zlib.decompress(decoded_data, -15)
        url_decoded = urllib.parse.unquote(decompressed_data.decode('utf-8'))
        return url_decoded
    except Exception as e:
        return None

def extract_labels_from_element(root):
    labels = []
    for elem in root.iter():
        value = elem.get('value')
        if value:
            clean_val = urllib.parse.unquote(value)
            clean_val = re.sub(r'<[^>]+>', ' ', clean_val)
            clean_val = re.sub(r'\s+', ' ', clean_val).strip()
            if clean_val:
                labels.append(clean_val)
        label = elem.get('label')
        if label:
            clean_val = re.sub(r'<[^>]+>', ' ', label)
            clean_val = re.sub(r'\s+', ' ', clean_val).strip()
            if clean_val:
                labels.append(clean_val)
    return list(set(labels))

dirs = [
    r"c:\Users\Admin\sim_magang_portofolio\documents\drawio_xml",
    r"c:\Users\Admin\sim_magang_portofolio\documents\drawio_xml\sequence_diagram"
]

for xml_dir in dirs:
    print(f"==================================================")
    print(f"  DIRECTORY: {xml_dir}")
    print(f"==================================================")
    for file in os.listdir(xml_dir):
        if file.endswith('.xml'):
            path = os.path.join(xml_dir, file)
            try:
                tree = ET.parse(path)
                root = tree.getroot()
                all_labels = []
                
                diagram_nodes = root.findall('.//diagram')
                if diagram_nodes:
                    for diag in diagram_nodes:
                        txt = diag.text.strip() if diag.text else ""
                        if txt:
                            decoded_xml_str = decode_drawio_diagram(txt)
                            if decoded_xml_str:
                                try:
                                    inner_root = ET.fromstring(decoded_xml_str)
                                    all_labels.extend(extract_labels_from_element(inner_root))
                                except Exception as parse_err:
                                    pass
                        all_labels.extend(extract_labels_from_element(diag))
                else:
                    all_labels.extend(extract_labels_from_element(root))
                    
                all_labels = list(set(all_labels))
                if all_labels:
                    print(f"=== File: {file} ===")
                    for lbl in sorted(all_labels):
                        print(f" - {lbl}")
                    print()
            except Exception as e:
                print(f"=== File: {file} (Error) ===")
                print(f" Error parsing: {str(e)}")
                print()
