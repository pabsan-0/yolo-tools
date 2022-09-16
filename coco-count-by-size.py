import json
import matplotlib.pyplot as plt
import numpy as np

"""
This script computes how many items in the a split (given as *.json) belong to each
coco size group.
"""

with open('test.json') as file:
    aa = json.load(file)

areas = [i['area'] for i in aa['annotations']]

plt.hist(areas, bins=30)
plt.axvline(x=32**2)
plt.axvline(x=96**2)


size = lambda area: 'small' if area < 32**2 else 'large' if area > 96**2 else 'medium'
groups = np.array([size(i) for i in areas])
print(f"""
small: {sum(groups == 'small')}
medium: {sum(groups == 'medium')}
large: {sum(groups == 'large')}
""")

plt.show()
