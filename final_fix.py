import json

def final_fix():
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

            # Encode to latin-1 and decode back to utf-8 to remove control characters
            cleaned_content = content.encode('latin-1', 'ignore').decode('utf-8')

            # Try to load and dump to format it nicely
            data = json.loads(cleaned_content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Successfully fixed {file_path}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

if __name__ == '__main__':
    final_fix()
