# var need change 
set PATH_debug_fpga_v   ./src/debug_fpga.v
set PATH_debug_xdc      ./src/debug_xdc.xdc

# var change occasionally
set SAMPLE_DEPTH   2048  
set SAMPLE_CLK     sub0_clkGen_i/sys_clk       

# var don't need to change
set InstName_Debug_FPGA_V   "debug_fpga_i/"


# ------- 1) analyze "debug_fpga.v" to get the debug signals list------------
set list_linesToDbg  {}
set list_netToDbg    {}
set list_busToDbg    {}
set items_to_dbg      {}

set fh_v [open $PATH_debug_fpga_v]
while { [gets $fh_v lineRd]!=-1} { 
    set linesSv [split $lineRd "\n"]
    foreach line $linesSv {
         #puts ":: $line"   		 
	     set matchDbg [string match {*mark_debug*} $line   ]   
	     if {$matchDbg} {
             lappend list_linesToDbg $line
	     }
    }
}
puts "---> $list_linesToDbg "
close $fh_v

# [regexp {( S+) s+!! s+( d+)} $line -> file num]

foreach lineDbg $list_linesToDbg {
    puts "::line to process:: $lineDbg"
    
	set matchNetBus [regexp  {\(\*.*\*\)\s*wire\s*(\[\s*(\d*)\s*:\s*(\d*)\s*\])?\s*(\w*)}  $lineDbg -- t1 t2 t3 t4]
    puts "net info: t1=$t1, t2=$t2, t3=$t3, t4=$t4"	
	if {$matchNetBus } {
	    if {$t2 == "" && $t3 == "" } {
		   lappend list_netToDbg  $t4 
		} else {

		   lappend list_busToDbg  $t4 
		}		    
	} else {
	    puts " XXXXXXXXX ERROR: lineDbg doesn't match eighther Net or Bus "
	}
    
}

# assemble nets
foreach netItemShort $list_netToDbg {
	lappend items_to_dbg  ${InstName_Debug_FPGA_V}/${netItemShort}
}
puts "===> items_to_dbg: $items_to_dbg"

# assemble buses
foreach busItemShort $list_busToDbg {
	lappend items_to_dbg  ${InstName_Debug_FPGA_V}/${busItemShort}[*]
}
puts "===+==> items_to_dbg: $items_to_dbg"

# ------- 2) analyze bus width--------------------
# --- open edif firstly
#open_run synth_1    # link_design -name netlist_1

# delete older
set num_debug_core [llength [get_debug_cores {u_ila_0 }] ]
if {  $num_debug_core >= 1  } {
    delete_debug_core [get_debug_cores {u_ila_0 }]
} else {
    puts "Note: the debug_core number is 0. No need to delete older."
}

set bus_width_0 [llength [get_nets $items_to_dbg   ]]

# ------ 3) make XDC content and write to file ----------
set xdc_string "set_property mark_debug true \[get_nets \[list $items_to_dbg ]]
  create_debug_core u_ila_0 ila    
  set_property ALL_PROBE_SAME_MU true         \[get_debug_cores u_ila_0]    
  set_property ALL_PROBE_SAME_MU_CNT    1     \[get_debug_cores u_ila_0]    
  set_property C_ADV_TRIGGER          false   \[get_debug_cores u_ila_0]     
  set_property C_DATA_DEPTH     $SAMPLE_DEPTH \[get_debug_cores u_ila_0]      
  set_property C_EN_STRG_QUAL false           \[get_debug_cores u_ila_0]       
  set_property C_INPUT_PIPE_STAGES      0     \[get_debug_cores u_ila_0]      
  set_property C_TRIGIN_EN            false   \[get_debug_cores u_ila_0]      
  set_property C_TRIGOUT_EN           false   \[get_debug_cores u_ila_0]      
  # ---sample clock connection                                                   
  set_property  port_width             1      \[get_debug_ports u_ila_0/clk]     
  connect_debug_port         u_ila_0/clk      \[get_nets \[list $SAMPLE_CLK ]]     


  # --- probe_0(probe_0 defaut has，no need to do <create_debug_port u_ila_0 probe> )    
  set_property PROBE_TYPE DATA_AND_TRIGGER    \[get_debug_ports u_ila_0/probe0]    
  set_property port_width $bus_width_0        \[get_debug_ports u_ila_0/probe0]    
  connect_debug_port u_ila_0/probe0           \[get_nets  \[list $items_to_dbg  ] ]      
                  

  # --- probe1(probe_1 need to do <create_debug_port u_ila_0 probe> )    
  # create_debug_port u_ila_0 probe     
  # set_property PROBE_TYPE DATA_AND_TRIGGER      \[get_debug_ports u_ila_0/probe1]    
  # set_property port_width  @@bus_width_111      \[get_debug_ports u_ila_0/probe1]    
  # connect_debug_port u_ila_0/probe1             \[get_nets  \[list {debug_fpga_i/wire_needDbg_1[*]}  ]]   

  # ----------------------- don't need change ------------------------------------------   
  set_property C_CLK_INPUT_FREQ_HZ   300000000 \[get_debug_cores dbg_hub]    
  set_property C_ENABLE_CLK_DIVIDER  false     \[get_debug_cores dbg_hub]    
  set_property C_USER_SCAN_CHAIN     1         \[get_debug_cores dbg_hub]    
  connect_debug_port   dbg_hub/clk             \[get_nets \[list $SAMPLE_CLK ]]     
"


set fh_xdc [open $PATH_debug_xdc w+]
puts $fh_xdc $xdc_string
close $fh_xdc

 
