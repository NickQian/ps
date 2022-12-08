#! /usr/bin/env python
# -*- coding: utf-8 -*-


import rtlpar
import util
import re


def scan_u_macros(fn_u, fn_prj_synp):
        #l_dic_defs, l_dic_undefs  = [], []
        
        #list_macro = get_u_macros(fn_u)
        #print("---> Info:<scan_u_macros> list u_macros to find:", list_macro)
       
        
        #for macro in list_macro:
        #        dic_def, dic_undef = defscan(macro, fn_prj_synp)
        #        l_dic_defs.append(   dic_def   )
        #        l_dic_undefs.append( dic_undef )
	dic_def, dic_undef = defscan(fn_u, fn_prj_synp)

	print ("Done:", dic_def, dic_undef)
	
	for key in dic_def:
        	print("Info:<scan_u_macros> MACRO: %s, Define FILE:%s"   %(key, dic_def[key]) )
	for key in dic_undef:
        	print("Info:<scan_u_macros> MACRO: %s, Undefine FILE:%s" %(key, dic_undef[key]) )

        return dic_def, dic_undef




# scan u module's macro `define XXX and `undef XXX
def defscan(fn_u, fn_prj_synp):
	#l_dic_defs, l_dic_undefs  = [], []
               
        dic_def   = {}
        dic_undef = {}

        list_macros = get_u_macros(fn_u)
        print("--> Info:<scan_u_macros> list u_macros to find:", list_macros)

	list_include_fn = get_u_include(fn_u)
	print("--> Info:<scan_u_macros> files already included:", list_include_fn)

        list_v, list_incdir = prj_to_vlist(fn_prj_synp)
        print ("--> Info:<defscan>   list_incdir:%s "%( list_incdir ) )

        #---- init the dicts
	for macro in list_macros:
        	dic_def[macro]   = []
        	dic_undef[macro] = []

        #--- .v search ---
	print ("start find macro in .v files...")
        for fn_v in list_v:
                lines_mod = []
                try:
                        with open(fn_v, mode='r') as f_v:
                                lines_mod = f_v.readlines()
                except IOError:
                        print ("Warning: cannot find file:%s" %(fn_v) )
                        
                for line in lines_mod:
			if rtlpar.line_has_define(line):
				for macro in list_macros:
                        		res_v_has_macro_def, res_v_has_macro_undef = linehas_macro_def(macro,  line)
                        		if res_v_has_macro_def:
                                		print ("====> res_v_has_macro_def:%s, fn:%s, line:%s "   %(res_v_has_macro_def, fn_v, line) )
						dic_def[macro].append(   [fn_v, line] )
                        		if res_v_has_macro_undef:
                                		print ("====> res_v_has_macro_undef:%s, fn:%s, line:%s " %(res_v_has_macro_undef, fn_v, line) )
                                		dic_undef[macro].append( [fn_v, line] )
		print("Info:finish file %s scan." %(fn_v) )
                                
                                
        #--- -include_path
        for incdir in list_incdir:
                list_h = util.get_flist_dir(incdir)
                print("----> <defscan> incdir: %s, list_h:%s" %(incdir, list_h) )
                
                for fn in list_h:
		    if fn in list_include_fn:
			print ("@@@@@@ fn %s already included in fn_u %s" %( fn, fn_u   ) )
		    else:
                        lines_h = []
                        fn_h = incdir+"/"+fn
                        try:
                                with open(fn_h, mode='r') as f_h:
                                        lines_h = f_h.readlines()
                        except IOError:
                                print (" ++++++ Warning: cannot find file:%s" %(fn_h) )
                       
			print("...processing file %s ... " %(fn) ) 
                        for line in lines_h:
				if rtlpar.line_has_define(line):
					for macro in list_macros:
                                		res_h_has_macro_def, res_h_has_macro_undef = linehas_macro_def(macro,  line)
                                		if res_h_has_macro_def:
                                			print ("====> res_h_has_macro_def:%s, fn:%s, line:%s "   %(res_h_has_macro_def,   fn_h, line) )
                                        		dic_def[macro].append( [fn_h, line] )
                                		if res_h_has_macro_undef:
                                			print ("====> res_h_has_macro_undef:%s, fn:%s, line:%s " %(res_h_has_macro_undef, fn_h, line) )
                                        		dic_undef[macro].append( [fn_h, line] )
			print("Info:finish file %s scan." %(fn_h) )
                                
                                        
        return dic_def, dic_undef

                                        

                                

def get_u_macros(fn_u):
        ptn_macro_use = r'`(\w+)'
        list_macro = []
        
        with open(fn_u, mode='r') as f:
                lines_u = f.readlines()

        for line in lines_u:
                #print ("===> is_ifdef_endif:", rtlpar.is_ifdef_endif(line) )
                if not rtlpar.is_ifdef_endif(line):
                        l_macro_line = re.findall(ptn_macro_use, line)
                        
                        if len(l_macro_line) > 1:    # if list, expand it
                                print ("-> l_macro_line > 1, l_macro_line:%s "%( l_macro_line) )
                                for macro in l_macro_line:
                                        if not (macro in list_macro):
                                                list_macro.append( macro )
                        elif len(l_macro_line) == 1:
                                print ("-> l_macro_line == 1, l_macro_line:%s "%( l_macro_line) )
                                if not (l_macro_line[0] in list_macro):
                                        list_macro.append( l_macro_line[0] )
                        
        return list_macro




def get_u_include(fn_u):
	ptn_include_file = r'`include\s*\"(\w+(\.v)|(\.h)|(\.vh)|(\.svh))\"'
	list_files_inc = []

	with open(fn_u, mode='r') as f:
                lines_u = f.readlines()

        for line in lines_u:
		res_match_include = re.search(ptn_include_file, line)
		if res_match_include is not None:
			print ("@@@ find include file: group(1):%s, group(2):%s " %( res_match_include.group(1), res_match_include.group(2)  ) )
			list_files_inc.append( res_match_include.group(1) )

	return list_files_inc



def linehas_macro_def(macro, line):
        #ptn_macro_def   = r'`define\s*{0}'.format(macro)
        #ptn_macro_undef = r'`undef\s*{0}'.format(macro)
        ptn_macro_def   = r'`define\s*{0}(\s+|\n)'.format(macro)
        ptn_macro_undef = r'`undef\s*{0}(\s+|\n)'.format(macro)
	match_def   = re.compile(ptn_macro_def)
	match_undef = re.compile(ptn_macro_undef)
        
        res_has_macro_def, res_has_macro_undef = False, False
        
        #res_match_macro_def   = re.search(ptn_macro_def,   line )
        #res_match_macro_undef = re.search(ptn_macro_undef, line )
        res_match_macro_def   = match_def.search(   line )
        res_match_macro_undef = match_undef.search( line )
        
        if res_match_macro_def is not None:
                res_has_macro_def   = True
        if res_match_macro_undef is not None:
                res_has_macro_undef = True

        return res_has_macro_def, res_has_macro_undef



        

def prj_to_vlist(fn_prj_synp):
        lines = []
        list_v, list_incdir = [], []
        
        with open(fn_prj_synp) as f:
                lines = f.readlines()

        for line in lines:
                if line.startswith("add_file"):
                        v_path = line.split(" ")[-1].lstrip('"').rstrip().rstrip('"\n')
			#print("+++> v_path:", v_path)
                        list_v.append(v_path  )
                if " -include_path " in line:
                        #inc_path = line.split(" ")[-1].lstrip('"').rstrip().rstrip('"\n')
                        list_inc_path = line.split(" ")[-1].strip().lstrip('{').rstrip('\n').rstrip('}').split(";")
			print("+(1)+> inc_path:", list_inc_path)
                        for inc_path in list_inc_path:
				print("+(2)+> inc_path:", inc_path)
                        	list_incdir.append(inc_path)

        #print ("Info:<prj_to_vlist>: list_incdir:%s" %( list_incdir) )
        return list_v, list_incdir
        




if __name__ == "__main__":
        fn_u        = "./demo_design/cmn700_naqu_smxp_e0n0_rni_rnd.v"
        fn_prj_synp = "./demo_design/css_0720_vu9p.prj"
        scan_u_macros(fn_u, fn_prj_synp)


        
