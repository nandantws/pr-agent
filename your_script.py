print('Hello worldww')

import os

for key, value in os.environ.items():
    print('===============')
    print(f"{key}: {value}")
