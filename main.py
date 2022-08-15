
#! /usr/bin/env python

import u2if
import mkif
import fmgen
#import fsgen


def main(fn_cfg):
	#dic_parSch = cfg_read(fn_cfg)
	
        u_name          = "u_userU"
	fn_caller       = "./real_v/ppa_top.v"
        fn_u            = "./real_v/userU_2001.v"
        fn_u_new        = "./real_v/userU_s2c.v"
        fn_user_axiIntf = "./real_v/axi_port_intf.v"
        fn_c2c_frame    = "./demo_design/c2c_frame.v"
	fn_fpga_top     = "./real_v/fpga_top.v"
        bank_num        = 'b237'

        fn_mkif_dest    = "./real_v/if_s2c.v"
        fn_fm           = "./real_v/fm.v"

	#1)---- mkif ----
        mkif.mkif(fn_caller, u_name, fn_u, fn_user_axiIntf, fn_mkif_dest)

	#2)---- fmgen ----
        fmgen.fmgen(fn_fpga_top, fn_u, fn_c2c_frame, fn_fm )

	#3)---- u2if ----
        u_proc = u2if.u_process(fn_caller, fn_u, u_name)   
        u_axi_intf_name = "axi_top_if"
        u_proc.u2if(fn_user_axiIntf, fn_u, u_axi_intf_name, fn_c2c_frame, bank_num, fn_u_new )

	#4) fsgen
	# fsgen()





if __name__ == "__main__":
	main("./config.info")

