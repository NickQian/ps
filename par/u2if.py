#! /usr/bin/env python
"""
empty the u, and replace the innner logic with INTF to fm.v 
"""

import rtlpar
import rtlproc

rtlparser = rtlpar.rtlpar()



# deal with all instances in 1 fpga process
def us_proc():

       	us = getUs(dic_parSch)

	u_proc = u_process()
	
	def __init__(self):
		for u in us:
			u_proc(u)
       
	def us_list(fns):
		pass

	#all instance to interface 
	def us2if():
		f2us, f3us, f4us = [""],[],[],[]
		dic_parSch = {fm:fpga_top, f2:f2us, f3:f3us, f4:f4us}





class u_process():

	def __init__(self, fn_caller, fn_u, u_name):
		self.u_dict = {}
		self.wrList = []	
		self.fn_caller = fn_caller
		self.u_name = u_name

	# get the instance info (dict)
	def getU(self):
		self.u_dict = rtlparser.uPars(self.fn_caller, self.u_name)
		self.wrList = self.u_dict['linesRd']     # init self.wrList
		return self.u_dict



	
	# get head str and turn it to list
	def get_u_modHead(self, fn_u_module ):
		listHead = []
		strHead, _  = rtlpar.getModuleHead(fn_u_module)
		return strHead.splitlines( keepends=False )



	def commentsU(self):
		print( "XXXX : lnum_u_start: %s, lnum_u_end:  %s"  %( self.u_dict['lnum_u_start'], self.u_dict['lnum_u_end']) )
		rtlproc.disableLines(self.fn_caller, self.u_dict['lnum_u_start'], self.u_dict['lnum_u_end'] )
		return True


	#def instIf(self):
	#	strIf =  "\n //-------- change to interface ----------- \n"
	#	strIf += "// *** axi_if ***  \n"
	#	strIf += self.u_dict["u_modName"] + "_sio_intf  u_sio_intf();  \n \n"
	#	strIf += self.u_dict["u_modName"] + "_intf" +  self.u_dict["u_name"] + "_intf ( \n"
	#	strIf += ".axi_if ( " + u_name_axi_intf + "), \n"
	#	strIf += ".sio_intf(u_sio_intf) ); \n\n " 
	#	return strIf


	#def connectSio(self ):
	##def conn2inside( ):
	#	strSio = '// sio connections \n'
	#	connWires  = self.u_dict['connWires'] 
	#	wiresInner = self.u_dict['wiresInner'] 
	#
	#	for wire in wiresInner:
	#		if rtlpar.is_ifdef_line(wire):
	#			strSio += wire + '\n'
	#		else:
	#			strSio += "assign u_sio_intf." + wire + " = " + wire + "; \n"; 
	#
	#	strSio += '// end sio connections \n'
	#
	#	return strSio


	def inst_axi_if(self, bank_num):
		strIf =  "\n //-------- c2c axi intf inst  ----------- \n"
		strIf += "c2c_frame_axi_if  u_c2c_" + bank_num + "_axi_if()/* synthesis syn_noprune=1 */ ; \n\n\n ";
		return strIf



	def inst_c2cFrame(self, fn_c2cFrame):
       		str_c2cFrame = "\n\n\n//----------------C2C frame inst----------------\n"

		str_c2cFrame += rtlproc.igen(fn_c2cFrame)
		
        	return str_c2cFrame

	
	# unpack the axi intf
	def connect_intf(self, fn_intf, u_axi_intf_name, bank_num):
		str_unpackIfs = "// unzip the intf : c2c input = slave input  \n "	
		dic_if = rtlparser.ifPars(fn_intf)  
        	for pinName in dic_if['pins']:
			print ("Info:<connect_intf>: pinName :%s" %( pinName ) )
                	str_unpackIfs += "assign u_c2c_" + bank_num + "_axi_if." + pinName +" = " + u_axi_intf_name + "." + pinName  + ";  \n"
		
		return str_unpackIfs


	


		



	def connectTdm(self):
		strTdm = '// Tdm connections \n'
		# more...

		strTdm = '// End Tdm connections \n'
		return strTdm




	def u2if(self, fn_intf, fn_u_module, u_axi_intf_name, fn_c2cFrame, bank_num, fn_u_new_mod ):
		
		#u_mod_lines = get_u_modHead()
		#lnum_head = len( u_mod_lines )
		
		#self.getU( )	          # get the u dict	
		#strIf  = self.instIf()
		#strSio = self.connectSio( )
		
		str_head, _ = rtlparser.getModuleHead(fn_u_module )
		str_head += "\n);"

		# generate Intf(axi/Sio/Tdm) connections
		str_c2c_axi_if  = self.inst_axi_if( bank_num )
		str_c2c_axi_if += self.connect_intf( fn_intf, u_axi_intf_name, bank_num)
		print ("Info:<u2if>: str_c2c_axi_if:%s " %( str_c2c_axi_if ) )

		str_inst_c2c_frame = self.inst_c2cFrame(fn_c2cFrame )	
		
		strTdm = self.connectTdm( )

		# insert the generated lines
		#self.wrList.insert(self.u_dict['lnum_u_end'] +1, wrStr)
		wrStr = str_head + str_c2c_axi_if + str_inst_c2c_frame + strTdm
		wrStr += "\n\nendmodule"

		with open(fn_u_new_mod, mode='w') as f: 
			#f.writelines( self.wrList )
			f.write( wrStr )
		print ("Info: <u2if> Write file %s done. " %(fn_u_new_mod) )

		#self.commentsU()
		print ("Info: <u2if> comments U done.")



	def u_mod2if(self, u_axi_intf_name ):
		self.getU( )              # get the u dict
		strIf = self.instIf( )	





if __name__ == "__main__":
	fn_caller       = "./demo_design/ppa_top.v"
	u_name          =  "u_userU" 
	fn_c2cFrame     = "./demo_design/c2c_frame.v"
	fn_user_axiIntf = "./demo_design/axi_port_intf.v" #generate the code with user axi bus intf. check it later
	fn_u            = "./demo_design/userU.v"
	fn_u_new        = "./demo_design/userU_s2c.v"
	
	u_proc = u_process(fn_caller, fn_u_module, u_name)   # 2022.8.13:fn_caller is not needed currently
	
	u_axi_intf_name = "axi_top2sys_if"
	bank_num        = 'b237'
	
	u_proc.u2if(fn_user_axiIntf, fn_u, u_axi_intf_name, fn_c2cFrame, bank_num, fn_u_new )
