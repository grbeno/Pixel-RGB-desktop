from PIL import Image
from matplotlib import pyplot as plt
import os

while 1:
	print('Add image path: \n<to exit press enter!>')
	inp = input()
	if inp == '':
		break
	try: 
		fname = os.path.join(inp)
		image = Image.open(fname) #.convert("LA")
	except:
		print('Hibás bemenet!')
		continue
	else: 
		plt.imshow(image)
		plt.show()
	


