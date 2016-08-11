class Rectangle(object):
		def __init__(self,x=0,y=0,width=10,height=10):
			self.setBounds(x=x,y=y,width=width,height=height);
		def setBounds(self,x=0,y=0,width=10,height=10):
			self.x = x;
			self.y = y;
			self.width = width;
			self.height = height;
			return self
		def setBoundsRect(self,rect):
			self.x = rect.x
			self.y = rect.y
			self.width = rect.width
			self.height = rect.height
			return self


		def __repr__(self):
			return reduce(lambda x,y:str(x)+" "+ str(y),[self.x,self.y,self.width,self.height])

		def removeFromLeft(self,a):
			self.x+=a
			self.width-=a
			return Rectangle(self.x-a,self.y,a,self.height)
		def removeFromTop(self,a):
			self.y+=a
			self.height-=a
			return Rectangle(self.x,self.y-a,self.width,a)
		def translate(self,x,y=0):
			self.x+=x
			self.y+=y
			return self
		def crop(self,x,y=0):
			self.width-=x
			self.height-=y
			return self



class UIParameter(Rectangle):
	""" base class for parameter widgets
	such class have a x,y,width,height field representing drawing coordinates in percentage [0..100] of the final window
	derived class can pass widget specific information thru UIparams dictionary

	"""
	allParams = set()
	
	def __init__(self,value=0,name='',x=0,y=0,width=10,height=10):
		self.hasChanged = False;
		self.allParams.add(self);
		self.__value = value
		self.name = name;
		self.listeners = {}
		self.__notifyingListeners = {}
		self.setCallbackFunction(self.onChange)
		# relative coordinates
		self.setBounds(x,y,width,height)

		# getting variable name if no name specified
		if(self.name == ''):
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

	def setCallbackFunction(self,callback):
		self.addListener('main',callback);
		return self


	def onChange(self,param):
		print "base change"
		pass

	def addListener(self,name,callback):
		def getValidCbFunction(f):
			import inspect
			if (len(inspect.getargspec(f)[0])==0):
				return lambda param:f()
			else :
				return f
		self.listeners[name]=getValidCbFunction(callback);
		self.__notifyingListeners[name] = False;
		return self

	def removeListener(self,name):
		if name in self.listeners:
			del self.listeners[name]
			del self.__notifyingListeners[name]



	def getValue(self):
		return self.__value


	def setValue(self, v):
		if(self.pyType):
			self.__value = self.pyType(v)
			print "set parameter "+self.name+" : "+ str(v)
		else:
			self.__value = v;
			print "set abstract parameter "+self.name + " : "+str(v)
		print self.listeners
		for k , cb in self.listeners.iteritems():
			if not self.__notifyingListeners[k]:
				self.__notifyingListeners[k] = True
				cb(param=self)
				self.__notifyingListeners[k] = False
		self.hasChanged = True;

	value=property(getValue,setValue)


class NumParameter(UIParameter):

	def __init__(self,value=0,name='',style='rotary',x=0,y=0,width=10,height=10):
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

	def __init__(self,value=False,name='',x=0,y=0,width=10,height=10):
		self.pyType = bool
		UIParameter.__init__(self,name=name,value=self.pyType(value),x=x,y=y,width=width,height=height)


class EventParameter(UIParameter):
	def __init__(self,name='',x=0,y=0,width=10,height=10):
		self.pyType = None
		UIParameter.__init__(self,name=name,value=None,x=x,y=y,width=width,height=height)


class EnumParameter(UIParameter):
	def __init__(self,choicesList = [],name='',value=0,x=0,y=0,width=10,height=10):
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
	
	def testCB():
		print "testCB"
		
	s3 = NumParameter(3,"lala",style="rotary").setBounds(1,2,16,16).setMinMax(0,1);
	lala = EnumParameter(choicesList = {"zala":"lala","lolo":["lili","lolou"]},value = 1).setBounds(1,2,16,16).setCallbackFunction(testCB);
	test2 = BoolParameter(False).setBounds(50,0,50,100)
	def dum():
		print 'dum'
	lala.addListener("L",dum)
	lala.value = ["zala"]
	# s2.value = ["lolo"]
	# for x in UIParameter.allParams:
	# 	print type(x).__name__
	# 	print x.getAttributeDict()
	# 	print '\n'
	

