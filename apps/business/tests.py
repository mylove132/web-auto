import json

string = '''
[{"cookieKey":"teacher_id","cookieValue":"adb5d5e3b75f4ec38b9ae99ca5c8182e"},{"cookieKey":"org_id","cookieValue":"80"}]

'''
li = json.loads(string)
for kay in li:
   print(kay['cookieKey'])

request_type_index = (
        (1, 'GET'),
        (2, 'POST'),
        (3, 'DELETE')
    )
for req in request_type_index:
    print(req[0])
    print(req[1])