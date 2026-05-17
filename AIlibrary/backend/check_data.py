import json

with open('mock_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(f'Loaded {len(data)} books')
    print('First 5 titles:')
    for book in data[:5]:
        print(f'  - {book["title"]}')
    print('Last 5 titles:')
    for book in data[-5:]:
        print(f'  - {book["title"]}')