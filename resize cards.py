import PIL
from PIL import Image

cards=[]
numbers=['A','2','3','4','5','6','7','8','9','10','J','Q','K']
suits=['C','S','H','D']

#resize
for i in suits:
    for z in numbers:
        cards=cards+[z+i]
print cards
basewidth = 65

for card in cards:
    path='/Users/jamieharris/Documents/Poker/Card Images/'+card+'.jpg'
    img = Image.open(path)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    z=card[:-1]+card[-1].lower()
    print z
    img.save('/Users/jamieharris/Documents/Poker/Card Images/'+z+'.jpg')


