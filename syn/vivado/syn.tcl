#!/bin/bash

# copy this syn.tcl to your our synthesis work dir. go to that dir.
# usage: $vivado -mode tcl -source  <your synthesis work dir>/syn.tcl
#

set XdcFile  ~/ps/synth.xdc
set Top_Module  fpga_top
# step 0: define output directory

set outputDir  <change to your synthesis work dir>


# step 0: raw list read in
list vline
set fp [open vlist.txt  r]
while { ![eof $fp]}{
	gets $fp vline
}


cancat list1  list2 list3
len=llenth{list1}
lappend list1 {list to add}

#use string? 



# step 1: setup design sources and constraints

read_verilog -sv [glob ./hdl/*.v]

read_xdc  $XdcFile

# step 2: run synthesis.
synth_design -top  Top_Module  -part xcvu...
# write_ceckpoint -force $outputDir/post_synth
#report_timing_summary -file $outputDir/post_synth_timing_summary.rpt


# for pr script, see "pr.tcl"  
