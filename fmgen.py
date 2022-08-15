
#! /usr/bin/env python

import rtlpar
import rtlproc
import rdcfg


c2c_port = """  input 	     bank_237_gt_refclk_clk_p,
		input 	     bank_237_gt_refclk_clk_n,
		input  [0:1] bank_237_gt_rxp,  bank_237_gt_rxn,
		output [0:1] bank_237_gt_txp,  bank_237_gt_txn,
		output       bank237_check_error,
           """
sx_c2c_bank_axi_if = "c2c_b237_axi_if"
#sx_tdm_intf        = "s1_tdm_intf"


rtlparser = rtlpar.rtlpar()


def fmgen(fn_fpga_top, fn_u, fn_c2c_frame, fn_fm):

	hie_ux = rdcfg.get_us_cfg()["f2"]   # temp
	modName = rtlpar.hie_to_moduleName( hie_ux )
	#hie_ux_if = ux_hie + ".u_if_" + modName
	print ("@1@<fmgen> ux_hie:%s, modName:%s " %( hie_ux,  modName )  )

	# get u's & c2c_frame module pin info to dict
	u_pinDic  = rtlparser.getModulePinsDic(fn_u)
	cf_pinDic = rtlparser.getModulePinsDic(fn_c2c_frame)
	print ("@2@<fmgen> u_pinDic:%s, cf_pinDic:%s " %( u_pinDic,  cf_pinDic )  )


	# 1) add c2c serdes ports / sio intf / tdm intf
	strFm = "// fm.v: fpga_top plus IO interfaces.  \n"
	strFm += "module fm #( )( " + c2c_port    
	strFm += "// SIO partitions  \n"
	strFm += modName + "_sio_intf.asPorts  sx_sio_intf,  \n"	
	strFm += "// tdm partitions  \n"
        strFm += "//" + modName + "_tdm_intf.asPorts  sx_tdm_intf,  \n"	

	# 2) copy user top ports
	pinList_fpgaTop = rtlparser.getModulePins(fn_fpga_top)
	print ("@3@<fmgen> pinList_fpgaTop:", pinList_fpgaTop )
        strFm += '\n'.join( pinList_fpgaTop )
	strFm += "); \n"

	# 3)------- inst user top ------
        usrTopName = rtlpar.fn_to_moduleName(fn_fpga_top)
	strFm += instUserTop(usrTopName)


	# 4)------ inst c2c frame & Intf ----
	"""
	strFm += "\n\n\n\n//-------------- inst c2c frame & Intf --------------  \n"
	strFm += "c2c_frame_axi_if  " + sx_c2c_bank_axi_if + "( ); \n"   # this is inst. needs ()
	strFm += inst_c2cFrame(fn_c2cFrame)
	"""

	# 5)------- make connections to SIO ------- 
	
	# 5.1) sio intf 
	strFm += "\n\n\n\n//------------------- sio_intf --------------------  \n"
	strFm += "//----- fm.output|inout = u.input ----- \n"
	for pinOut in u_pinDic['input']:	
		strFm += "assign  sx_sio_intf." + pinOut   + " = " + "u_"+hie_ux + "." + pinOut  + ";  \n"


	
	strFm += "//----- u.output = fm.input ----- \n "
	for pinIn in u_pinDic['output']:
		strFm += "assign  " + "u_"+hie_ux + "."  +  pinIn    + " = " + "sx_sio_intf." + pinIn + ";  \n"
	for pinInout in u_pinDic['inout']:
		strFm += "assign  " + "u_"+hie_ux + "."  +  pinInout + " = " + "sx_sio_intf." + pinInout  + ";//inout  \n"

	# 5.2) tdm intf
	# strFm += "assign " + sx_tdm_intf + " = " + "u_"+hie_ux_if + ".tdm_if"

	#5.3) c2c frame serdes pins( for axi intf)
	strFm += "\n\n\n\n//------------------- c2c serdes pins: axi_intf --------------------  \n"
	
	strFm += "//----- (c2c_frame).input = fm.input --- \n "
	for serdesPinIn in cf_pinDic['input']:
		 strFm += "assign " + "u_"+hie_ux + "."+serdesPinIn + " = " +  serdesPinIn + " ; \n"    # ????
	
	strFm += "//----- fm.outut = (c2c_frame).output --- \n"
	for serdesPinOut in cf_pinDic['output']:
		strFm += "assign " + serdesPinOut + " = " + "u_"+hie_ux + "."+serdesPinOut + "; \n" 	

	# 6) end
	strFm += "\n endmodule  \n "

	with open(fn_fm, mode='w+') as f:
                f.write(strFm)
        print ("Info: write fm file %s done. " %(fn_fm) )




def isPortLine (lineStr):
	if line.lstrip().startswith("input") or line.lstrip().startswith("output") or line.lstrip().startswith("inout"):
        	return True
        elif line.lstrip().startswith("`ifdef") or line.lstrip().startswith("`endif"):
		return True
        else:
		return False
	 

# not use igen(). becasue the ports are same and connect to fm directly. 
def instUserTop(userTopName):
	str = "//--------------- user top instant-------------------\n"
	str += userTopName + " u_" + userTopName + "( .*);  \n"
	return str






# hybrid connection = c2c + sio + tdm
def inst_hc_s1():
	pass




#def inst_c2cFrame(fn_c2cFrame):
#	str = "//----------------C2C frame inst----------------\n"
#	str += rtlproc.igen(fn_c2cFrame)
#
#	return str 	







#######
def inst_s1_if(s1_modname):
	str = "//////// f2/3/4/5 ... ////////"
	str += "s1_if " + s1_modname + "#()( .*); "
	return str


def connect_s1():
	pass	
	
	

		



if __name__ == "__main__":
        fn_fpga_top      = "./demo_design/fpga_top.v"
	fn_u             = "./demo_design/userU.v"
	fn_c2c_frame     = "./demo_design/c2c_frame.v"
        fn_fm            = "./demo_design/fm.v"
        fmgen(fn_fpga_top, fn_u, fn_c2c_frame, fn_fm )