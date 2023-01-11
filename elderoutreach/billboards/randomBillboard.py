from os		import popen,	system
from random	import choice,	randint
from sys import argv

INDE	= ["in", "de"]

try:
	system("rm out.png")
except:
	pass
emojis	= popen("ls | grep png | grep -v base").read().split()
suburbs = []
f = open("suburbs", "r")
for l in f.readlines():
	suburbs.append(l.strip())
f.close()
percentage	= randint(1, 9)
suburb		= choice(suburbs)
inorde		= choice(INDE)
emoji		= choice(emojis)

volunteers = ['Queensland Community Care Network', 'Anglicare SQ', 'Able Australia Services', 'St Stephens Meals on Wheels', "St Vincent's Care Services", 'Lutheran Services', 'Volunteering Redlands Inc', 'Wesley Mission Queensland', 'Regis Aged Care Pty Ltd']

rand_volun = randint(0, len(volunteers) - 1)

top = f"{suburb}'s senior citizens are feeling"
bottom = f"Community wellbeing {inorde}creased by {percentage}% this month"
top_2 = f"{volunteers[rand_volun]}".center(50, " ")
print(top_2)

middle =  "is looking for volunteers!"
bottom_2 = f"Make a difference. Help out today."
system(f"magick base.png {emoji} -layers flatten -font './SansitaOne.ttf' -pointsize 64 -fill '#1A1525' -annotate +400+250 \"{top}\" -annotate +200+1000 \"{bottom}\" out.png")
system(f"magick base.png logo-f.png -layers flatten -font './SansitaOne.ttf' -pointsize 64 -fill '#1A1525' -annotate +560+250 \"{top_2}\" -annotate +550+330 \"{middle}\" -annotate +450+1000 \"{bottom_2}\" 2out.png")
#if "-bsd" in argv:
#	system(f"./igen-bsd {suburb} {inorde} {percentage} {emoji} out.png")
#else:
#	system(f"./igen {suburb} {inorde} {percentage} {emoji} out.png")
