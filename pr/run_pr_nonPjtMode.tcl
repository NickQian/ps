# NOTE: typical usage would be "vivado -mode batch -source <this_Tcl_script>

# ----------------------- STEP#0: ----------------------------------------------------------------
set EdfFile           ./src/fpga_top.edf
set outputDir         ./output
#file mkdir $outputDir
set FN_Fpga_org_xdc ./src/test.xdc
set FN_Fpga_Debug_xdc ./debug_xdc.xdc

#set_param
set_property target_part xcvu19p-fsva3824-1-e  [current_fileset -constrset]

# ---------------------- STEP#1: ----------------------------------------------------------------
read_edif  $EdfFile
# --Reads the .sdc or .xdc format constraints source files for the Non-Project Mode session.
read_xdc  $FN_Fpga_org_xdc   
     # add_files  -fileset constrs_1 -norecurse   $FN_Fpga_Debug_xdc
     # import_files -fileset constrs_1 -force     $FN_Fpga_Debug_xdc


# STEP#2: run synthesis, report utilization and timing estimates, write checkpoint design
#synth_design -top bft -part xc7k70tfbg484-2
#write_checkpoint -force $outputDir/post_synth
#report_timing_summary -file $outputDir/post_synth_timing_summary.rpt


# --------------------- STEP#2:  link design & gen debug xdc -------------------------------------
link_design
source ./src/genDbgXdc.tcl
puts " =====gen Dbg Xdc ok ====== "
read_xdc  $FN_Fpga_Debug_xdc   

# --------------------- STEP#3: run opt_design, place -------------------------------------------
opt_design
place_design
phys_opt_design
write_checkpoint -force $outputDir/post_place
report_timing_summary -file $outputDir/post_place_timing_summary.rpt

# -------------------- STEP#4: router, report,run drc, write xdc out ----------------------------
route_design
write_checkpoint -force $outputDir/post_route
report_timing_summary -file $outputDir/post_route_timing_summary.rpt
report_timing -sort_by group -max_paths 100 -path_type summary -file $outputDir/post_route_timing.rpt
#report_clock_utilization -file $outputDir/clock_util.rpt
#report_utilization -file $outputDir/post_route_util.rpt
#report_drc -file $outputDir/post_imp_drc.rpt

write_xdc -no_fixed_only -force $outputDir/xdcWrited.xdc

# --------------------- STEP#5: bitstream ---------------------------------------------------------
write_bitstream -force $outputDir/bft.bit

