class Rectangle(object):

		def setBounds(self,x=0,y=0,width=10,height=10):
			self.x = x;
			self.y = y;
			self.width = width;
			self.height = height;
			return self


class UIParameter(Rectangle):
	""" base class for parameter widgets
	such class have a x,y,width,height field representing drawing coordinates in percentage [0..100] of the final window
	derived class can pass widget specific information thru UIparams dictionary

	"""
	autoName = True
	allParams = set()
	def __init__(self,name='',value=0,x=0,y=0,width=10,height=10):
		self.hasChanged = False;
		self.allParams.add(self);
		self.__value = value
		self.name = name;

		# relative coordinates
		self.setBounds(x,y,width,height)

		# getting variable name if no name specified
		if(self.name == '' and UIParameter.autoName):
			import inspect,re
			className = str(type(self).__name__)
			regx =re.compile('.*\=.*'+className+'.*\(')
			frames = inspect.getouterframes(inspect.currentframe())
			found = False
			for f in frames:
				codeLine = f[4][0]
				if(regx.match(codeLine)):
					self.name = codeLine.split('=')[0].lstrip().rstrip()
					break;

	def getAttributeDict(self):
		members = {attr:getattr(self,attr) for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__")}
		return members


	def __del__(self):
		print "del"
		self.allParams.remove(self);

	def setCallBackFunction(self , f):
		self.onChange = f
		return self


	def onChange(self,param):
		print "base change"
		pass
	



	def getValue(self):
		return self.__value

	def setValue(self, v):
		if(self.pyType):
			self.__value = self.pyType(v)
			print "set "+ str(v)
		else:
			self.__value = v;
			print "trigger " + str(v)
		self.onChange(param=self)
		self.hasChanged = True;

	value=property(getValue,setValue)


class NumParameter(UIParameter):

	def __init__(self,name='',value=0,style='rotary',x=0,y=0,width=10,height=10):
		if(type(value) not in [int,float]):
			value = float(value)
			print ( "wrong parameter type for NumParameter, assigning to float")
		self.pyType = type(value)
		UIParameter.__init__(self,name=name,value=self.pyType(value),x=x,y=y,width=width,height=height)
		self.style = style;
		self.min  = 0;
		self.max  = 0;
		


	def setMinMax(self,_min,_max):
		self.min = self.pyType(_min);
		self.max = self.pyType(_max);
		return self



class BoolParameter(UIParameter):
	def __init__(self,name='',value=False,x=0,y=0,width=10,height=10):
		self.pyType = bool
		UIParameter.__init__(self,name=name,value=self.pyType(value),x=x,y=y,width=width,height=height)


class EventParameter(UIParameter):
	def __init__(self,name='',x=0,y=0,width=10,height=10):
		self.pyType = None
		UIParameter.__init__(self,name=name,value=None,x=x,y=y,width=width,height=height)


class EnumParameter(UIParameter):
	def __init__(self,name='',choicesList = [],value=0,x=0,y=0,width=10,height=10):
		self.pyType = None
		self.choicesList = choicesList
		UIParameter.__init__(self,name=name,value=value,x=x,y=y,width=width,height=height)

	def setValue(self, v):
		print "overriden"
		if(type(v)==int):
			v=self.getValueForIndex(v)
		if type(v)==list and len(v)>0 and all([type(x)==str for x in v]):
			def getChild(dic,plist):
				if type(dic) != dict: return None
				if len(plist)==1:
					return dic[plist[0]]
				else:
					return getChild(dic[plist[0]],plist[1:])
			v = getChild(self.choicesList,v)

		UIParameter.setValue(self,v);

	def getValueForIndex(self,idx):
		def getElemAtIdx(parent,startIdx,destIdx):
			print((parent))
			if type(parent)==list:
				for a in parent:
					startIdx , elem = getElemAtIdx(a,startIdx,destIdx)
					if elem != None:
						return startIdx,elem
				return startIdx+len(parent),elem
			elif type(parent) == dict:
				for a in parent.itervalues():
					startIdx , elem = getElemAtIdx(a,startIdx,destIdx)
					if elem != None:
						return startIdx,elem
				return startIdx+len(parent),elem
			else:
				if startIdx==destIdx:
					return startIdx,parent
				else :
					return startIdx+1,None
		dumb,res = getElemAtIdx(self.choicesList,0,idx)
		return res


			


	value=property(UIParameter.getValue,setValue)

if __name__== "__main__":
	
	def testCB(param):
		print "testCB"
		
	s3 = NumParameter("lala",value=3,style="rotary").setBounds(1,2,16,16).setMinMax(0,1);
	s2 = EnumParameter(name="lala",choicesList = {"zala":"lala","lolo":["lili","lolou"]},value = 1).setBounds(1,2,16,16).setCallBackFunction(testCB);
	test2 = BoolParameter().setBounds(50,0,50,100)
	
	s2.value = ["lolo"]
	for x in UIParameter.allParams:
		print type(x).__name__
		print x.getAttributeDict()
		print '\n'
	

