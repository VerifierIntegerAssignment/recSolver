
_N1=100
def y4(_n1):
	if _n1==0:
		return 50
	else :	
		if (((_n1-1)+0)<50) : 
			return y4((_n1-1))
		else : 
			return (y4((_n1-1))+1)

try:
	print y4(_N1)
except Exception as e:
	print "Error(InstQuery)"