#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os


# get on dir's file list    
def get_flist_dir(incdir):
    flist     = []
    res_flist = []
    try:
        flist = os.listdir(incdir)
    except:
        print("Warning: cannot find incdir path specified: %s" %(incdir) )
    
    for fn in flist:    	
            cur_path = os.path.join(incdir, fn)
        
            if os.path.isdir(cur_path):
                    get_flist_dir(cur_path)
            else:
                    #if some_special_name in fn:
		    #print("+++3+++>", fn)
                    res_flist.append(fn)
                
    #print ("@@1<get_flist_dir>: incdir: %s, res_flist: %s" %(incdir, res_flist ) )
    return res_flist
