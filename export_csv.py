import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path

def parse_health_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    records = []
    for record in root.findall('.//Record'):
        rec_dict = record.attrib
        rec_dict['type'] = rec_dict.get('type', '')
        records.append(rec_dict)
    
    return pd.DataFrame(records)

# Usage
df = parse_health_xml('Export.xml')
print(df.head())
df.to_csv('health_data.csv', index=False)
