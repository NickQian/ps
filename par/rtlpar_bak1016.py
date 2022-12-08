#! /usr/bin/env python/

# rtl parser

import re


ptn_comment     = r'^\s*\/\/'
match_com       = re.compile(ptn_comment)

ptn_mod_head    = r'module\s*\w+\s*[#\s*[(].*[)] ]?\s*[(](.*)[)]\s*;'
match_mod_head  = re.compile(ptn_mod_head, re.M|re.S)

ptn_module      = r'module\s+(\w+)'
match_mod       = re.compile(ptn_module)

#ptn_m_parameterStart     = r'^.*#\(\s*'
#match_m_parameterStart   = re.compile(ptn_m_parameterStart)

ptn_mod_parameter = r'parameter\s*(\w+)\s*=.*'    # module parameter lines
match_mod_param   = re.compile(ptn_mod_parameter)

#ptn_m_parameterEnd = r'[)]\s*[^;]$'
#match_m_paramEnd      = re.compile(ptn_m_parameterEnd)


ptn_mod_signal_95  = r'(output|input|inout)\s*.*(?=;)'
ptn_mod_signal     = r'(output\s*.*|input\s*.*|inout\s*.*)'
#ptn_mod_signal     = r'(output|input|inout)(\s+|\[).*'
match_mod_signal   = re.compile(ptn_mod_signal)

ptn_intf_pins    = r'(wire|logic)(\s+|\[.*\])+\s*(\w+)\s*;'
match_intf_pins  = re.compile(ptn_intf_pins)


ptn_mod_end       = r'^\s*endmodule'
match_mod_end     = re.compile(ptn_mod_end)

#--------- unit instance -------

ptn_u_parameterStart     = r'^.*#\s*[(]\s*[.]\.*'    #   # ( .AXI3_LEN
match_m_parameterStart   = re.compile(ptn_u_parameterStart)





class rtlpar:
	STATE ={"BigComments"  : ['IN_BIG_COMMENTS', 'OUT_BIG_COMMENTS' ],  \
		"Section"      : ['IN_MODULE_HEAD',  'IN_U',  'END_U',    'IN_95_PIN_DECLARE',  'IN_MOD_BODY',  ], \
		"Segment"      : ['IN_PARAMETER',  'IN_2001_PIN_DECLARE', 'IN_95_PIN_NAMES',    'IN_U_DECLARE', 'IN_PIN_CONN',  'IN_ALWAYS',  'IN_ASSIGN'  ],  \
		"IfDef"        : ['IN_IFDEF',      'OUT_IFDEF'           ]   \
		} 


	def __init__(self ):
		self.u_dict = {  'u_name'      : '',    'u_modName' :'', 
				 'lnum_u_start': None , 'lnum_u_end':None,   'linesRd'   :[],  
			         'paramLines'  : [],    'params'    :[],                               
				 'connLines'   : [],    'connWires' :[],     'wiresInner':[],
				 'connPair'    :{},     'conPair_'  :{}
				}

        	self.m_dict = { 'mod_name'   : '',  'syntax_95' : None,
				'paramLines' : [],  'params'    : [  ], 'lnum_paramDecl_start': None, 'lnum_paramDecl_end': None,
        			'pinLines'   : [],  'pins'      : [  ], 'lnum_pinDecl_start'  : None, 'lnum_pinDecl_end'  : None
				}
		
		self.if_dict = {'intf_name'  : '',
				'pinLines'   : [],  'pins' : [] 
				}
	
		#--- init state keys
		self.state = { } 
		keyList_state = rtlpar.STATE.keys()
		for key in keyList_state:
			self.state[key] = ''
	
	# module analyse
	def mPars(self, fn):
		getModulePins(fn)                  # use the 1st );
		
		with open(fn, mode='r') as f:
			self.m_dict['linesRd'] = f.readlines()
		
		# traverse the module
		lcnt = 0
              	for line in self.m_dict['linesRd']:
			lcnt += 1
			
			if see_left_BigComments( line ) and (not has_synDirective(line) ) :
                                self.state["BigComments"] = 'IN_BIG_COMMENTS'
                                print ("---> IN_BIG_COMMENTS", line )
                        if see_right_BigComments( line ) and (self.state["BigComments"] == 'IN_BIG_COMMENTS'):
                                self.state["BigComments"] = 'OUT_BIG_COMMENTS'
                                print ("---> OUT_BIG_COMMENTS", line )

			line = line.lstrip()                                 # remove head space firstly
                        comments_mc, module_mc, end_mc = rtlparser.line_judge(line)
		
			if (not self.state["BigComments"] == 'IN_BIG_COMMENTS') and (not is_commentLine(line) ):
                        	#if module_mc:
                        	#        mod_name = module_mc.group(1)
				if line.startswith("module"):
					self.m_dict['mod_name'] = line.split(str=" ")[2]
					self.state["Section"]   = 'IN_MODULE_HEAD'
					print("@1@ Info:<mpars>: module name is %s " %self.m_dict['mod_name'] )

                        	if match_mod_param.findall(line):
					if self.state["Section"] == 'IN_MODULE_HEAD':
				        	self.m_dict['lnum_paramDecl_start'] = lcnt
				
                                	self.state["Segment"]   = 'IN_PARAMETER'
                                	self.m_dict['paramLines'].append(line)
					self.m_dict['params'].append( paramLine_to_param(line) )
        				print("@2@ Info:<mpars>: params:%s, params[1:]:%s, sigs:%s  \n" %( params, params[1:], sigs ))

                        	if match_mod_signal.findall(line):
					if self.m_dict['syntax_95']  == False:
						if self.state["Segment"] == 'IN_PARAMETER':
							self.m_dict['lnum_paramDecl_end'] = lcnt -1
							self.m_dict['lnum_pinDecl_start'] = lcnt
							self.state["Segment"] == 'IN_2001_PIN_DECLARE'
						#self.m_dict['pinLines'].append(line)
						self.m_dict['pins'].append( pinLine_to_pin(line) )
                                		print("@3@ Info:<mpars>: pinLine_to_pin:%s" %(pinLine_to_pin(line) ) )
					else:   # if syntax_95
						self.state["Section"] == 'IN_95_PIN_DECLARE'

					if see_BraSemi(line) and (self.state["Segment"] == 'IN_2001_PIN_DECLARE'):
						self.state["Section"] = 'IN_MOD_BODY'
						print("@4@ Info:<mpars>: In MOD_BODY..."  )

                        	if end_mc:
                                	print("@5@ Info:<mpars>: END Module Parse."  )
                                	break

			return self.m_dict




	# analyze 1 u with u_name
	def uPars(self, fn_module, u_name):
		lcnt = 0
		self.u_dict['u_name'] = u_name
		#lnum_u_para_start, lnum_u_para_end                 = None, None
		#lnum_u_pin_conn_start, lnum_u_pin_conn_end         = None, None
		linesModule = []

		
		#--- read the fn
		with open(fn_module, mode='r') as f:
			self.u_dict['linesRd'] = f.readlines()
		strRd = ''.join( self.u_dict['linesRd'] )
		self.u_dict['u_modName'] =  u_to_moduleName(strRd, u_name)

	
		for line in self.u_dict['linesRd']:
			lcnt += 1
			if see_left_BigComments( line ) and (not has_synDirective(line) ):
				self.state["BigComments"] = 'IN_BIG_COMMENTS'
				print ("---> IN_BIG_COMMENTS", line )
			if see_right_BigComments( line ) and self.state["BigComments"] == 'IN_BIG_COMMENTS':
				self.state["BigComments"] = 'OUT_BIG_COMMENTS'
				print ("---> OUT_BIG_COMMENTS", line )
			
			if not self.state["BigComments"] == 'IN_BIG_COMMENTS':	
				if line.lstrip().startswith(u_name):
					self.state["Section"] = 'IN_U'
					self.state["Segment"] = 'IN_U_DECLARE'
					self.u_dict['lnum_u_start'] = lcnt
					#str_containsU = ''.join(self.u_dict['linesRd'][lcnt-20:lcnt+2] )
					#print ("----> str_containsU: %s" %(str_containsU) )
					#self.u_dict['u_modName'] =  u_to_moduleName(str_containsU, u_name)
				
				if self.state["Section"] == 'IN_U' and self.state["Segment"] == 'IN_U_DECLARE':
					self.state["Segment"] = 'IN_PIN_CONN'
					self.u_dict['connLines'].append(  line  )
				
				if self.state["Section"] == 'IN_U' and self.state["Segment"] == 'IN_PIN_CONN':
					if see_BraSemi(line):
						self.state["Section"] = 'END_U'
						self.u_dict['lnum_u_end'] = lcnt
						break    # jump out the 'for'
					else:
						if not is_commentLine(line):
							self.u_dict['connLines'].append( line )			
                
		self.u_dict['connWires']  =  getUconnection( self.u_dict['connLines'] ) 
		# add "not PAD wires" as wiresInner 
		self.u_dict['wiresInner'] =  getUconnNopad( self.u_dict['connWires'] )
		print("Info:<uPars>: u_dict[connWires]: ", self.u_dict['connWires']  )
		print("Info:<uPars>: u_dict[wiresInner]:", self.u_dict['wiresInner'] )		

		return self.u_dict	


	




	def ifPars(self, fn_intf):
		with open(fn_intf, mode='r') as f:
                        self.if_dict['linesRd'] = f.readlines()

                # traverse the module
                lcnt = 0
                for line in self.if_dict['linesRd']:
                        lcnt += 1

                        if see_left_BigComments( line ) and (not has_synDirective(line) ):
                                self.state["BigComments"] = 'IN_BIG_COMMENTS'
                                print ("--> IN_BIG_COMMENTS, state['BigComments']:", self.state["BigComments"] )
                        if see_right_BigComments( line ) and (self.state["BigComments"] == 'IN_BIG_COMMENTS'):
                                self.state["BigComments"] = 'OUT_BIG_COMMENTS'
                                print ("<-- OUT_BIG_COMMENTS", line )

                        line = line.lstrip()                                 # remove head space firstly

                        if (not self.state["BigComments"] == 'IN_BIG_COMMENTS') and (not is_commentLine(line) ):
				#print("Info:@1<ifPars>: line is:%s" %(line) )
				if ifLine_to_ifName(line) is not None:
					self.if_dict['intf_name'] = ifLine_to_ifName(line)
				
				res_pinSearch = match_intf_pins.search(line)
				if res_pinSearch is not None:
					self.if_dict['pinLines'].append( res_pinSearch.group(0) )
					self.if_dict['pins'].append( res_pinSearch.group(3) )
					#print("Info:@2<ifPars>:res.group(0):%s,(3):%s" %(res_pinSearch.group(0), res_pinSearch.group(3) ) )

		print ("Info:@3<ifPars>: self.if_dict[intf_name]:%s,if_dict[pinLines]:%s, if_dict[pins]:%s" %(self.if_dict['intf_name'], self.if_dict['pinLines'], self.if_dict['pins']) )

		return self.if_dict



	def define_par():
		pass



	def define_scan(fl):
		#list_define = []   # all files
		dic_define = {}    # in a file
		vlist = get_vlist(fl)
		
		for fn_v in vlist:
			dic_define[fn_v] = mod_define_scan(fn_v)
			#list_define.append()
	
		return dic_define


	# find the 1st ); to get the module head
        def getModuleHead(self, fn_module):
                str_head, str_body= "", ""

		list_fn = self.fn2noCmntList(fn_module)
                str_mod = ''.join(list_fn) 
		#with open(fn_module, mode='r') as f:
                #        str_mod = f.read()
                
		str_head, _str, str_body = str_mod.partition(");")       # <partition> only process the 1st match
		
		return str_head, str_body

	
	# also get syntax_1995(2001) info
	def getModulePins(self, fn_module):
		portList = []
		str_head, str_body = self.getModuleHead(fn_module)
		#print ("@1@<getModulePins>: fn:%s, str_head: %s" %( fn_module,  str_head )  )
		portList_v2001 = match_mod_signal.findall(str_head)
		portList_v1995 = match_mod_signal.findall(str_body)
		print ("@2@<getModulePins>: portList_v2001:%s, portList_v1995:%s" %( portList_v2001, portList_v1995 ))
		if   len(portList_v2001) != 0:
			self.m_dict['syntax_95'] = False
			portList = portList_v2001
		elif len(portList_v1995) != 0:
			self.m_dict['syntax_95'] = True
			portList = portList_v1995
		else:
			print ("@3@<getModulePins>: Error: len(portList_v2001) & 1995 are all zero! \n ")
		
		self.m_dict['pinLines'] = portList 
		
		print ("@3@<getModulePins>: self.m_dict['syntax_95']:%s, self.m_dict['pinLines']:%s " %(self.m_dict['syntax_95'] ,self.m_dict['pinLines']  ) )
		return portList


	
	def getModulePinsDic(self, fn_mod):
		pinList = self.getModulePins( fn_mod )
		pinDic  = pinLines_to_PinDic(pinList)	
		print ("XXXXX <getModulePinsDic>, pinList:%s, pinDic:%s" %(pinList, pinDic) )
		return pinDic
		


	def line_judge(self, line):
		comments_match = match_com.match(line)
                module_match   = match_mod.match(line)
                end_match      = match_mod_end.search(line)
		return comments_match, module_match, end_match


	# read fn, remove comments lines, return list
	def fn2noCmntList(self, fn):
                linesModule = []

 		lcnt = 0
                #--- read the fn
                with open(fn,  mode='r') as f:
                        self.u_dict['linesRd'] = f.readlines()

                for line in self.u_dict['linesRd']:
                        lcnt += 1
                        if see_left_BigComments( line ) and (not has_synDirective(line) ):
                                self.state["BigComments"] = 'IN_BIG_COMMENTS'
                                print ("---><fn2noCmntList>: IN_BIG_COMMENTS", line )
			if (self.state["BigComments"] != 'IN_BIG_COMMENTS') and (not  is_commentLine(line) ):
				linesModule.append(line)
                        if see_right_BigComments( line ) and (self.state["BigComments"] == 'IN_BIG_COMMENTS'):
                                self.state["BigComments"] = 'OUT_BIG_COMMENTS'
                                print ("<---<fn2noCmntList>: OUT_BIG_COMMENTS", line )

		return linesModule
				

#=================== pattern match functions ============================

def fn_to_moduleName(fn):
	ptn_fn2modName = r'/([a-zA-Z0-9_]+)[.]v|[sv]$'
	mmatch = re.compile(ptn_fn2modName)
	return ''.join( mmatch.findall(fn) )



def hie_to_moduleName(str_hie):
	ptn_hie2modName = r'.u_([a-zA-Z0-9_]+)$'
	hie2mmatch  = re.compile(ptn_hie2modName)
	moduleName = ''.join( hie2mmatch.findall(str_hie) )
	#print ("@1@<hie_to_moduleName> str_hie:%s, moduleName:%s" %(str_hie, moduleName) )
	return moduleName



def u_to_moduleName(str, u_name):
	print ("Info:<u_to_moduleName>: u_name:%s " %(u_name ) )
	#ptn_u_to_moduleName = r'(\w+)\s*(#\s*\(.*\))?\s*{0}'.format(u_name)
	ptn_u_to_moduleName = r'(\w+)\s*(#.*)?\s*{0}'.format(u_name)
	match_u_modName = re.compile(ptn_u_to_moduleName, re.M|re.S)   # S:.include\n
	res_match       = match_u_modName.search(str)
	print("<u_to_moduleName>: search result res_match.group(1):", res_match.group(1) )
	return res_match.group(1)

def modLine_to_modName(line):
	ptn_module      = r'module\s+(\w+)'
	match_mod       = re.compile(ptn_module)
	res_match       = match_mod.search(line)
	return res_match.group(1)

def ifLine_to_ifName(line):
	ptn_intf      = r'interface\s+(\w+)'
        match_intf      = re.compile(ptn_intf)
        res_match       = match_intf.search(line)
	if res_match is not None:
        	return res_match.group(1)
	

def paramLine_to_param(line):
	ptn_mod_paramName   = r'parameter\s*(\w+)\s*=.*$'    # module parameter lines
	match_mod_paramName = re.compile(ptn_mod_parameter)
	return ''.join( match_mod_paramName.findall(line) )



def pinLine_to_pin(line):
	#ptn_mod_sigName    = r'output\s*(.*)|input\s*(.*)|inout\s*(.*)[;]|[,]\s*$'
	#ptn_mod_sigName    = r'[output\s*|input\s*|inout\s*]([a-zA-Z0-9._]+)\s*[;|,|\s*\n]'
	ptn_mod_sigName     = r'(output|input|inout)(\s+|\[.*\])+\s*([a-zA-Z0-9._]+\s*(\s*\[\w+\]\s*)?)'
	match_mod_sigName   = re.compile(ptn_mod_sigName)
	res_match = match_mod_sigName.search( line )
	print("Info<pinLine_to_pin>: res_match.group(1):%s, group(2):%s, group(3):%s, group(4):%s"  %(res_match.group(1), res_match.group(2), res_match.group(3), res_match.group(4) ) )
	
	#if res_match.group(4) is not None:
	#	return res_match.group(3) + res_match.group(4)
	#else:
	#	return res_match.group(3)
	return res_match.group(3)




def pinLines_to_PinDic(lines):
	pinDic =       {'input' : [], 
			'output': [],
			'inout' : []  
		} 
	
	for line in lines:
		if not ( isPadPin(line) ):
			if isInputPin(line):
				pinDic['input'].append(  pinLine_to_pin(line) )
			if isOutputPin(line):
				pinDic['output'].append( pinLine_to_pin(line) )
			if isInoutPin(line):
				pinDic['inout'].append(  pinLine_to_pin(line) )
	return pinDic



#def getUconnDirection(self, fn_called, u_name):
# output: [('phy_d1_pad_C', 'stpu_phy_d1_pad_C')]
def isPadPin( pinLine ):
        ptn_pad   = r'_pad|_PAD|_Pad|_If|_if|_intf|_INTF'    # remove 
        match_pad = re.compile(ptn_pad)
        return match_pad.search( pinLine )  


def isInputPin ( pinLine ):
	ptn_input = r'\s*input(\s+|\[)+'
	match_input = re.compile(ptn_input)
	return match_input.search( pinLine ) 

def isOutputPin( pinLine ):
	ptn_output = r'\s*output(\s+|\[)+'
	match_output = re.compile(ptn_output)
	return match_output.search( pinLine )

def isInoutPin ( pinLine ):
	ptn_inout = r'\s*inout(\s+|\[)+'
	match_inout = re.compile(ptn_inout)
	res_match = match_inout.search( pinLine )
	if res_match is not None:
		print("Info:<isInoutPin>: res_match.group(0):%s, pinLine:%s" %( res_match.group(0), pinLine ) )
	return res_match



def is_ifdef_endif(line):
        ptn_ifdef_endif = r'(`ifdef|`else|`endif|`include|`undef|`timescale)(\s+|\n)'
        return re.search(ptn_ifdef_endif, line)

def line_has_define(line):
	ptn_ifdef_endif = r'(`define\s+)'
	return re.search(ptn_ifdef_endif, line)



def uConn_to_connWire(line):
	#ptn_uConn_wire = r'[(]\s*([a-zA-Z0-9._]+)\s*[)]\s*,?\s*$'
	ptn_uConn_wire = r'[.]([a-zA-Z0-9._]+)\s*[(]\s*([a-zA-Z0-9._]+)\s*[)]\s*,?\s*$'
	wireMatch = re.compile(ptn_uConn_wire) 
	return wireMatch.findall(line)


def pinDeclare_to_define(line):  # input [P_NUM_SUBSYS-1:0] AVDDU_A_DDR
	if is_ifdef_line(line):
		return ''
	else:
		ptn_pinDecl2def = r'(\w+\s*(\[.*\])?)\s*\w+'
		matchDef = re.compile( ptn_pinDecl2def )
		res_search = matchDef.search(line)
		#print("XXXX5: res_search.group(1): %s, res_search.group(2):%s " %(res_search.group(1), res_search.group(2) ) )
		return res_search.group(1)



def see_BraSemi(line):
	ptn_BracketSemicolon = r'[)]\s*;'
	braSemiMatch = re.compile(ptn_BracketSemicolon)
	return braSemiMatch.search(line)




def see_left_BigComments(line):
	ptn_lbc = r'/[*]'
	lbc_match = re.compile(ptn_lbc)
	return lbc_match.search(line)



def see_right_BigComments(line):
        ptn_rbc = r'[*]/'
        rbc_match = re.compile(ptn_rbc)
	res_match = rbc_match.search(line)
	if res_match:
		print(">see */" )
        return res_match



def has_synDirective( line ):
	if see_left_BigComments(line) and see_right_BigComments(line):
		print ("> has_synDirective:", line)
		return True
	else:
		return False


# deal with //
def is_commentLine( line ):
	comments_match = match_com.match(line)
	if comments_match:
		#print ("=> is comments line:", line )
		return True
	
	#return comments_match







def is_ifdef_line(line):
	ptn_ifdef = r'(`ifdef\s*\w+)|(`endif\s*)'
	match_ifdef = re.compile(ptn_ifdef)

	if not isinstance(line, str):
		line_str = ''.join(line)
	else:
		line_str = line

	res_search = match_ifdef.search(line_str)
	if res_search is not None:
		return res_search.group()
	else:
		return False



#=============== get/find functions  ============================

def find_connWireDeclare(connWireList, fn_caller):
	lines = []
	listDeclare = []
	with open(fn_caller, mode='r') as f:
		lines = f.readlines()
	
	for connWire in connWireList:
		if isinstance(connWire, str):
			if is_ifdef_line(  connWire  ):
				listDeclare.append( connWire )
		for line in lines:
			ptn_rtlVarDeclare = r'(input|output|inout|assign|wire)\s+(\[.*\])?\s*{0}\s*(\[.*\])?'.format(connWire)
			match_connWireDeclare = re.compile(ptn_rtlVarDeclare)
			res_search = match_connWireDeclare.search(line)
		
			if not is_commentLine(line):
				if res_search is not None:
					listDeclare.append( res_search.group() )
					#print ("Info:<find_connWireDclare>, line processing is:%s, res_search.group() is: %s" %(line, res_search.group() ) )

	print ("Info:<find_connWireDeclare> listDeclare is:", listDeclare)
	return listDeclare




# find original declaration 
def find_connPinDeclare(connPinList, fn_u):
        lines = []
        listDeclare = []
        with open(fn_u, mode='r') as f:
                lines = f.readlines()

        for connPin in connPinList:
		if isinstance (connPin, str):
			if is_ifdef_line( connPin ):
				listDeclare.append(connPin)    # add `ifdef lines
        	for line in lines:
			ptn_pinDeclare = r'(input|output|inout)\s+(\[.*\])?\s*{0}\s*(\[.*\])?'.format(connPin)
        		match_pinDeclare = re.compile(ptn_pinDeclare)
                	res_search = match_pinDeclare.search(line)

                	if not is_commentLine(line):
				if res_search is not None:
                        		listDeclare.append( res_search.group() )
                        		#print("XXXX4: res_search.group() is: ",  res_search.group() )

        print ("Info:<find_connPinDeclare> pin listDeclare is:", listDeclare)
        return listDeclare




# get U's connections wire. 
# return a list
def getUconnection( connLines ):
	connWires = []
	for line in connLines:
		line_ifdef = is_ifdef_line(line)
		if line_ifdef:
			connWires.append( line_ifdef )
			
		wire =  uConn_to_connWire(line)
		if len(wire) > 0:
			connWires.append( wire )
	return connWires





#def getUconnDirection(self, fn_called, u_name):
# output: [('phy_d1_pad_C', 'stpu_phy_d1_pad_C')]
def getUconnNopad( connWires ):
	connWires_Nopad = []
	ptn_pad   = r'_pad|_PAD|_Pad|_If|_if|_intf|_INTF'    # remove 
        match_pad = re.compile(ptn_pad)	
	for wire in connWires:
		#print ("info:<getUconnNopad> wire: %s " %( wire ) )
		
		if isinstance(wire, str):  # `ifdef MC_DFI_X64_A
			if is_ifdef_line( wire ):  
				connWires_Nopad.append(wire)
		elif not match_pad.search( ''.join(wire[0][1])):  # [('AVDDU_A_DDR', 'AVDDU_A_DDR_STPU_in')]
			connWires_Nopad.append( wire[0][1] )
	
	return connWires_Nopad





# u_dict[wiresInner]:without _pad.   ['subsys_pu_inner_wire', 'AVDDU_A_DDR_STPU_in']
# u_dict[connWires] :has the relationship.  [ [('subsys_pu', 'subsys_pu_inner_wire')], [('AVDDU_A_DDR', 'AVDDU_A_DDR_STPU_in')], '`ifdef MC_DFI_X64_A'] 
def getInnerWireDir(wiresInner, connWires, fn_u):
	pinList4intf = []

	# from C find the corresponding pin B. 
	for wireInner in wiresInner:
		if  is_ifdef_line( wireInner ):   #('`ifdef' in wireInner) or ('`endif' in wireInner):
			pinList4intf.append(wireInner)
		for connPair in connWires:
			if isinstance(connPair, list):    # avoid the '`ifdef' lines
				if connPair[0][1] == wireInner:   
					pinList4intf.append(connPair[0][0])


	pinDeclares = find_connPinDeclare(pinList4intf, fn_u)
	#print ("Info<getInnerWireDir>: pinList4intf:", pinList4intf )
	print ("Info<getInnerWireDir>: pinDecclares:", pinDeclares )

	return pinDeclares, pinList4intf




def getABCDlist(wiresInner, connWires, fn_caller, fn_u):
        # get A-B-C-D list ( input[]B,  .B(C),  input[]C )
        #                    ---A-------B---C------D------
        abcdList =  []
        pinDeclares, pinList4intf = getInnerWireDir( wiresInner, connWires, fn_u)   # A, B
        wireInnerDeclares         = find_connWireDeclare(wiresInner,  fn_caller)      # D

        w_cnt = 0
        for innerWire in wiresInner:
                abcdList.append( [pinDeclares[w_cnt], pinList4intf[w_cnt], innerWire, wireInnerDeclares[w_cnt] ] )
                w_cnt += 1

        print ("Info<getABCDlist>: abcdList:", abcdList)
	return abcdList


	
def getAClist(wiresInner, connWires, fn_caller, fn_u):
	acList, abcList = [], []

	abcdList = getABCDlist( wiresInner, connWires, fn_caller, fn_u )
	
	# form the acList
	for e in abcdList:
		#acList.append( [ pinDeclare_to_define(e[0]), e[2] ])
		abcList.append( [ (e[0]), e[1], e[2] ])
	print ("Info<getAClist>: abcList:", abcList)

	acList = replace_BwithC(abcList)
	print ("Info<getAClist>: acList:" , acList)

	return acList





# use replace becuase
def replace_BwithC(abcList):
	list_ac = []
	for abc in abcList:
		ac = abc[0].replace(abc[1], abc[2])	
		list_ac.append(ac)
	return list_ac


#------------------ ???? ------------------
# get the whole pin lines
# output: string
#def getModPinStr(fn_src_mod):
#	rtlparser = rtlpar()
#        pinsList = rtlparser.getModulePins(fn_src_mod)
#        str_Pins = '\n'.join(pinsList)
#	return str_Pins




#------------------- for local call ---------------------------
def get_vlist(fl):
	lines = []
	vlist  = []
	ptn_v_file = r'\s+([a-zA-Z0-9_/]+\w+.(v|sv|h|svh))\s*$'
	
	with open(fl, mode='r') as f:
		lines = f.readlines()
	for line in lines:
		res_search = re.search(ptn_v_file, line)
		if res_search is not None:
			vlist.append(res_search.group() )
	
	print ("Info:<define_scan> get v lists:", vlist)
	return vlist


def mod_define_scan(fn_v):
	ptn_def_undef = r'(`define\s*\w+)|(`undef\s*\w+)'
	lines = []
	defList = []

	with open(fn_v, mode = 'r') as f:
		lines = f.readlines(fn_v)

	for line in lines:
		res_search = re.search(ptn_def_undef, line)
		if res_search is not None:
			defList.append(res_search.group() )

	return defList








if __name__ == "__main__":
        fn  = "./demo_design/ppa_top.v"
	rtlparser = rtlpar()
	print("---> getUconnection: ", rtlparser.getUconnection(fn, "u_userU") )

