import json

def fix_json_files_manually():
    files_to_fix = {
        'ba_polity_v5.json': {
            'line': 8,
            'old': '• **1986 का संशोधन:** अब जन्म के समय माता या पिता में से किसी एक का भारत का नागरिक होना अनिवार्य है। [cite: 1075]',
            'new': '• **1986 का संशोधन:** अब जन्म के समय माता या पिता में से किसी एक का भारत का नागरिक होना अनिवार्य है। [cite: 1075]'
        },
        'ba_polity_v8.json': {
            'line': 8,
            'old': '• **अगस्त प्रस्ताव (1940):** पहली बार संविधान सभा की मांग को ब्रिटिश सरकार ने आधिकारिक रूप से स्वीकार किया।',
            'new': '• **अगस्त प्रस्ताव (1940):** पहली बार संविधान सभा की मांग को ब्रिटिश सरकार ने आधिकारिक रूप से स्वीकार किया।'
        },
        'ba_polity_v10.json': {
            'line': 8,
            'old': '• **समानता का अधिकार (अनुच्छेद 14-18):** कानून के समक्ष समानता, धर्म, जाति, लिंग या जन्म स्थान के आधार पर भेदभाव का निषेध।',
            'new': '• **समानता का अधिकार (अनुच्छेद 14-18):** कानून के समक्ष समानता, धर्म, जाति, लिंग या जन्म स्थान के आधार पर भेदभाव का निषेध।'
        },
        'ba_polity_v11.json': {
            'line': 9,
            'old': '• **राज्य पुनर्गठन अधिनियम, 1956:** इस अधिनियम के तहत भारत में 14 राज्य और 6 केंद्र शासित प्रदेश बनाए गए।',
            'new': '• **राज्य पुनर्गठन अधिनियम, 1956:** इस अधिनियम के तहत भारत में 14 राज्य और 6 केंद्र शासित प्रदेश बनाए गए।'
        }
    }

    for file_path, fix_info in files_to_fix.items():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Remove any character that is not a standard printable character
                        cleaned_content = "".join(c for c in content if c.isprintable() or c in '\n\r\t')
        
                    data = json.loads(cleaned_content)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    print(f"Successfully fixed {file_path}")
        
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
if __name__ == '__main__':
    fix_json_files_manually()
