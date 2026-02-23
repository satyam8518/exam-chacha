import json

file_path = 'mp_special_list.json'
data = []

for i in range(1, 16):
    file_name = f'sub_mp_special_v{i}.json'
    with open(file_name, 'r', encoding='utf-8') as f:
        content = json.load(f)
        item = {}
        if 'subjectId' in content:
            item['subjectId'] = content.get('subjectId')
            item['subjectTitle'] = content.get('subjectTitle')
            item['contentUrl'] = f"https://exam-chacha.pages.dev/{content.get('subjectId')}.json"
        else:
            item['subjectId'] = content.get('id')
            item['subjectTitle'] = content.get('title')
            item['contentUrl'] = content.get('contentUrl')

        if 'iconName' in content:
            item['iconName'] = content.get('iconName')
            item['colorHex'] = content.get('colorHex')
        else:
            if i == 1:
                item['iconName'] = 'map'
                item['colorHex'] = '#FF9800'
            else:
                item['iconName'] = 'book'
                item['colorHex'] = '#4CAF50'
        data.append(item)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
