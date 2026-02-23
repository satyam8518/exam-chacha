import json

def fix_json_files():
    files_to_fix = [
        'ba_polity_v5.json',
        'ba_polity_v8.json',
        'ba_polity_v10.json',
        'ba_polity_v11.json'
    ]

    for file_path in files_to_fix:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove control characters
            cleaned_content = content.encode('utf-8', 'ignore').decode('utf-8')

            data = json.loads(cleaned_content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Successfully fixed {file_path}")

        except json.JSONDecodeError as e:
            print(f"Error processing {file_path} after cleaning: {e}")
        except Exception as e:
            print(f"An unexpected error occurred with {file_path}: {e}")


if __name__ == '__main__':
    fix_json_files()
