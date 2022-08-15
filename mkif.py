#! /usr/bin/env python

import rtlpar

rtlparser = rtlpar.rtlpar()



def mkif( fn_caller, u_name, fn_u, fn_user_axiIntf, fn_dest):
	# modname, modports, modparams = rtlpar.mPars(fn)
	ifStr = if_gen( fn_caller, u_name, fn_user_axiIntf, fn_u )

	with open(fn_dest, mode='w+') as f:
		f.write(ifStr)
		#f.writelines(str + "\n" )  # write_lines([])
	print ("Info: write intf file %s done. " %(fn_dest) )	


def axi_if_cpUser(fn_user_axiIntf):
	str_axi_if  = "\n\n//------------- copy user axi inerface -------------\n"
	if_dict = rtlparser.ifPars(fn_user_axiIntf)
	with open(fn_user_axiIntf, mode='r') as f:
		str_axi_if += f.read()

	str_axi_if = str_axi_if.replace(if_dict['intf_name'], " c2c_frame_axi_if ")  
	return str_axi_if	


def if_gen(fn_caller, u_name, fn_user_axiIntf, fn_u ):
	u_dict = rtlparser.uPars(fn_caller, u_name)
	modName = u_dict['u_modName']       #modName = rtlpar.fn_to_moduleName(fn_module)
	#modPins = rtlparser.getModulePinStr(fn_module)
	list_connWireDeclare = rtlpar.find_connWireDeclare(u_dict['wiresInner'], fn_caller)  
	

	#ac_list  = rtlpar.getAClist(  u_dict['wiresInner'], u_dict['connWires'], fn_caller, fn_u )
	abcd_list = rtlpar.getABCDlist(u_dict['wiresInner'], u_dict['connWires'], fn_caller, fn_u )


	# 1)----- total intf ---------
	ifStr = "interface "+ modName + "_intf ( input bit clk);  \n" + \
                "axi_port_intf.master   axi_if;                   \n" + \
		modName + "_sio_intf    sio_intf;                 \n" + \
		modName + "_tdm_intf    tdm_intf;                 \n" + \
 		"endinterface \n\n"


	# 2)------- sio-----------
	ifStr += "interface "+ modName + "_sio_intf (   );  \n"
	pinStr = ""


	#--logic 
	#for connWireLine in list_connWireDeclare:    # if no "," or it's "`ifdef|`endif", just keep that line
	for abcd in abcd_list:
		#pinStr += connWireLine.replace("input" ,  "   logic")\
		pinStr += ''.join(abcd[0]).replace("input" ,  "   logic")\
                                          .replace("output",  "   logic")\
                                          .replace("inout" ,  "   wire ")\
				          .replace("assign",  "   logic")\
                                          .replace(",", "")                # remove ',' 

		# if define line, no ';'
		if  rtlpar.is_ifdef_line( abcd ): 
                        pinStr +=  ' \n'
                else:
                        pinStr +=  ';\n'

	ifStr += pinStr 


	#--modport 
	
	ifStr += "\n\n\n modport asPorts (" 
	

	#list_m_if_pin = reverse_s_if_pin(list_s_if_pin)
	a_str = ''
	a_cnt = 0
	for abcd in abcd_list:
		a_cnt += 1
		if rtlpar.isInputPin(abcd[0]):    # abcd[0] is a
			a_str += (  ''.join(abcd[0])   ).replace("input" ,  "  output")
		elif rtlpar.isOutputPin(abcd[0]):
			a_str += (  ''.join(abcd[0])   ).replace("output",  "  input" )
		elif rtlpar.isInoutPin(abcd[0]):
			a_str += (  ''.join(abcd[0])   )


		# define line copy
		if rtlpar.is_ifdef_line(abcd[0]):
			a_str += abcd[0] + '\n'
		elif  ( a_cnt == len(abcd_list)  ):  # if not (define line) and not (last line), no ','
			a_str +=  ' \n'
		else:
			a_str +=  ',\n'

		#print("Info:<if_gen>:a_cnt:%s,  a_str:%s" %(a_cnt,  a_str) )	

	ifStr += a_str + "); \n"
	ifStr +=  "\n endinterface     \n\n"


	# 3)-------- tdm ---------
	ifStr += "interface "+ modName + "_tdm_intf (   );    \n"
	ifStr += "// TODO "
	ifStr +=  "\n endinterface    \n\n"


	# 4)-------- user axi intf copy& modify---------
	ifStr += axi_if_cpUser(fn_user_axiIntf)

	return ifStr






if __name__ == "__main__":
	fn_caller    = "./demo_design/ppa_top.v"
        u_name       = "u_userU"
	fn_u         = "./demo_design/userU.v"
        fn_user_axiIntf = "./demo_design/axi_port_intf.v"
	fn_dest      = "./demo_design/if_s2c.v"
        
	mkif(fn_caller, u_name, fn_u, fn_user_axiIntf, fn_dest)