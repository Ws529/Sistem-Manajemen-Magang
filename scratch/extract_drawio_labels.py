import os
import xml.etree.ElementTree as ET
import urllib.parse

def extract_labels_from_xml(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        labels = []
        # Draw.io objects and mxCell elements
        for elem in root.iter():
            value = elem.get('value')
            if value:
                # Clean up HTML tags and unescape URL encoding if any
                clean_val = urllib.parse.unquote(value)
                # Simple HTML tags removal
                import re
                clean_val = re.sub(r'<[^>]+>', ' ', clean_val)
                clean_val = re.sub(r'\s+', ' ', clean_val).strip()
                if clean_val:
                    labels.append(clean_val)
            # Check label attribute too
            label = elem.get('label')
            if label:
                clean_val = re.sub(r'<[^>]+>', ' ', label)
                clean_val = re.sub(r'\s+', ' ', clean_val).strip()
                if clean_val:
                    labels.append(clean_val)
        return list(set(labels))
    except Exception as e:
        return [f"Error: {str(e)}"]

xml_dir = r"c:\Users\Admin\sim_magang_portofolio\documents\drawio_xml"
for file in os.listdir(xml_dir):
    if file.endswith('.xml'):
        path = os.path.join(xml_dir, file)
        labels = extract_labels_from_xml(path)
        print(f"=== File: {file} ===")
        for lbl in sorted(labels)[:25]: # limit to first 25 unique labels
            print(f" - {lbl}")
        print()
