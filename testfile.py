import re

full_name = "John-Doe"
valid = True

if re.search(r'[^a-zA-Z- ]', full_name) is not None:
    valid = False
    print(valid)
else:
    valid = True
    print(valid)