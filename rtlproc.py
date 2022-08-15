#! /usr/bin/env python

import rtlpar
 
rtlparser = rtlpar.rtlpar()


def igen(fn_mod):
	str_u = ''
	params=[]
	sigs =[]
	state_start = 0
	state_end   = 0
	mod_name = ''

	with open(fn_mod, mode = 'r') as f:
		lines_rtl = f.readlines()
		for line in lines_rtl:
			comments_mc, module_mc, end_mc = rtlparser.line_judge(line)
			#print("@1@ <igen>: line: %s, match_sig:%s " %(line, rtlpar.match_mod_signal.findall(line) ) )		

			if module_mc:
				mod_name = module_mc.group(1)
				state_start = 1
			if rtlpar.match_mod_param.findall(line):
				params.append( rtlpar.paramLine_to_param(line) )
			if rtlpar.match_mod_signal.findall(line):
				#print("@2@ <igen>  rtlpar.pinLine_to_pin:%s" %(rtlpar.pinLine_to_pin(line) ) )
				sigs.append(   rtlpar.pinLine_to_pin(line) )
			if end_mc:
				state_end = 1
				break
 
	inst_name = ' u_'+mod_name

	print("@3@ <igen> params:%s, params[1:]:%s, sigs:%s  \n" %( params, params[1:], sigs ))
	# mod_name and parameters and u_module
	if len(params) == 0:
		str_u = mod_name + inst_name + "( \n"
	else:
		str_u = mod_name + "#(" + ''.join(params[0]) +  ", \n"                                               # first parameter
		str_u += (''.join(params[1:]) ).replace("parameter", "\n ,parameter" ) + ")" + inst_name + "(" # if not first parameter

	# ports
	for sig in sigs[:-1]:
		str_u += "." + sig + "(  "  + sig   + "),         \n" 	  # if not last signal
	str_u += "." + sigs[-1] + "(  "  + sigs[-1] + "  )  );    \n\n"    # last signal

	# wires declaration
	for sig in sigs:
		str_u += "wire " + sig + " /* synthesis syn_noprune=1 */; \n "


	return str_u


# copy u's module heads input/output list to fn_dest 
def cpSubPorts(fn_src_mod, fn_dest):
        str_dest = ""
        rtlparser = rtlpar()
        portsList = rtlparser.getModulePins(fn_src_mod)
        str_instPorts = ''.join(portsList)
        lcnt = 0
        with open(fn_dest, mode='r+') as f:
                str_dest = f.read()
                dest_pre_str, _str, dest_post_str = str_dest.partition(");")
                str_dest = dest_pre_str + str_instPorts + ");" + dest_post_str

        print ("@2@ <cpSubPorts>: str_instPorts: %s, dest_pre_str:%s, dest_post_str:%s, str_dest:%s" %(str_instPorts,dest_pre_str, dest_post_str, str_dest) )


def disableLines(fn, lineStart, lineEnd):
	lcnt = 0
	wrlines = []
	with open(fn, mode='r+') as f:
		#print ("XXXX<disableLines> after open: fn.tell:", f.tell  )
		wrlines = f.readlines( )
		wrlines.insert(lineStart-2, '{0}\n'.format('/*  \n') )
		wrlines.insert(lineEnd+1,   '{0}\n'.format('*/  \n') )
		f.seek(0, 0)
		f.writelines(wrlines)

