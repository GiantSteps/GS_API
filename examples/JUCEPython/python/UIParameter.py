class UIParameter(object):

	def __init__(self,v,x,y,width,height):
		self.hasChanged = False;
		self.__value = v
		self.UIparams = {
		# relative coordinates
		"x":x,"y":y,"width":width,"height":height}



	def onChange(self):
		print "base change"
		pass

	def getValue(self):
		return self.__value

	def setValue(self, v):
		self.__value = v
		print "set "+ str(v)
		self.onChange()
		self.hasChanged = True;

	value=property(getValue,setValue)



if __name__== "__main__":
	p = UIParameter(1);
	p2 = UIParameter(2);
	print p._UIParameter__value
	print p.value,p2.value
	p.value = 10
	p2.value = 20
	print p,p2.value
	

