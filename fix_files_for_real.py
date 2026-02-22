import json

def fix_json_files_for_real():
    files_to_fix = [
        'ba_polity_v5.json',
        'ba_polity_v8.json',
        'ba_polity_v10.json',
        'ba_polity_v11.json',
    ]

    for file_path in files_to_fix:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
        
                    # More aggressive cleaning
                    cleaned_content = ''.join(c for c in content if 31 < ord(c) < 127 or c in '\n\r\t' or ord(c) > 127)
        
                    # Try to load and dump to format it nicely
                    data = json.loads(cleaned_content)
                    
                    new_file_path = file_path.replace('.json', '_fixed.json')
                    with open(new_file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    print(f"Successfully cleaned {file_path} and created {new_file_path}")
        
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
if __name__ == '__main__':
    fix_json_files_for_real()
