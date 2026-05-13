from ai_assistant import generate_response

tests = [
    'Optimize this: worked on projects and did good things',
    'Suggest keywords for: Python, Django, REST APIs',
    'Write a cover letter for Software Engineer at Google, my name is John Smith',
]

for test in tests:
    print(f'User: {test}')
    resp = generate_response(test)
    print(f'{resp}')
    print('-' * 70)
    print()
