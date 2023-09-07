print('Hello worldww')

import os

for key, value in os.environ.items():
    print('===============')
    print(f"{key}: {value}")
    if "BITBUCKET_PR_ID" in key:
        print('PR ID found')
