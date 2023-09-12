print('Hello worldww')

import os
bitbucket_bearer_token = os.environ.get("BITBUCKET_BEARER_TOKEN")
print(f"bearer: {bitbucket_bearer_token}===============================")

for key, value in os.environ.items():
    print('===============')
    print(f"{key}: {value}")
    if "BITBUCKET_PR_ID" in key:
        print('PR ID found')
