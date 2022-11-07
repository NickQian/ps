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

