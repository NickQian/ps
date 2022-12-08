#!/bin/bash

#----------------- Changable vars ---------------------
FN_FLIST=soc_emu.f

DIR_FLIST_ROOT=/emu2/palladium/nld_s2c/
#STR_EMU_PATH=/emu2/palladium/nld_s2c
TOP_MODULE=fpga_top

DEFINE_COMPILER_FILE=define_compiler.svh
SOURCEME_FILE=SourceMe

fn_in=$DIR_FLIST_ROOT$FN_FLIST
fn_out=./syn.tcl


echo "============== start process ... fn is:$fn_in ================"
source ./subfunc.sh

#-------- tcl set global var --------
echo "set EMU_PATH $STR_EMU_PATH" >> $fn_out

#------- set global defines for compiler -----------
echo "add_file -verilog ./desinge_compiler.svh" >> $fn_out

#------- set top module name for synplify prj -----
echo "set_option -top_module ${TOP_MODULE}" >> $fn_out

#-------- synthesize configuration ---------------
echo "  set_option -project_relative_includes       0
	set_option -dup                             1
	set_option -looplimit                    5000
	set_option -fix_gated_and_generated_clocks  1
	set_option -disable_io_insertion            1
" >>  $fn_out

#---- process .f file --------
casep_dotf $fn_in  $DIR_FLIST_ROOT   $fn_out
echo $Vlines >>  $fn_out

echo "<--------------------- END----------------------------"



