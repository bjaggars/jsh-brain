import sys
from PIL import Image
ns=sys.argv[2:]; ims=[Image.open(f'cap/{n}.jpg').resize((443,960)) for n in ns]
s=Image.new('RGB',(453*len(ims),960),'white')
for i,im in enumerate(ims): s.paste(im,(453*i,0))
s.save(sys.argv[1],quality=72)
