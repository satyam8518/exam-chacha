import json
import os

def create_master_search():
    master_search_list = []
    
    # Base URL for the content
    base_url = "https://exam-chacha.pages.dev/"

    # List of subject files to process
    subject_files = [f for f in os.listdir('.') if f.endswith('_subjects.json')]

    for subject_file in subject_files:
        with open(subject_file, 'r', encoding='utf-8') as f:
            subject_data = json.load(f)
            for subject in subject_data.get('subjects', []):
                # Add subject entry
                master_search_list.append({
                    "title": subject.get('title'),
                    "type": "subject",
                    "url": subject.get('contentUrl')
                })

                # Fetch and process the class list file
                class_list_file = subject.get('contentUrl').split('/')[-1]
                if os.path.exists(class_list_file):
                    with open(class_list_file, 'r', encoding='utf-8') as cf:
                        class_data = json.load(cf)
                        class_list = []
                        if isinstance(class_data, dict):
                            class_list = class_data.get('subjects', [])
                        elif isinstance(class_data, list):
                            class_list = class_data
                        
                        for class_item in class_list:
                            # Add class entry
                            class_url = class_item.get('contentUrl')
                            master_search_list.append({
                                "title": class_item.get('title') or class_item.get('subjectTitle'),
                                "type": "class",
                                "url": class_url
                            })

                            # Fetch and process the class content file
                            class_content_file = class_url.split('/')[-1]
                            if os.path.exists(class_content_file):
                                try:
                                    with open(class_content_file, 'r', encoding='utf-8') as ccf:
                                        content = ccf.read()
                                        # More aggressive cleaning
                                        cleaned_content = ''.join(c for c in content if 31 < ord(c) < 127 or c in '\n\r\t' or ord(c) > 127)
                                        content_data = json.loads(cleaned_content)
                                except json.JSONDecodeError as e:
                                    print(f"Error decoding JSON from file: {class_content_file}")
                                    print(e)
                                    continue
                                parent_class_title = content_data.get("subjectTitle")
                                for topic in content_data.get('topics', []):
                                        for question in topic.get('questions', []):
                                            # Add question entry
                                            master_search_list.append({
                                                "title": question.get('questionText'),
                                                "type": "question",
                                                "parentClass": parent_class_title,
                                                "url": class_url
                                            })

    with open('master_search.json', 'w', encoding='utf-8') as f:
        json.dump(master_search_list, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    create_master_search()
