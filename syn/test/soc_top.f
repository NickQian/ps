//test1.f

./arch_package1.sv

//-f $PRJ/sub3/test3.f
-f $PRJ/test2.f


$PRJ/./ddr4_model1.sv
$PRJ/./ddr4_sdram_model_wrapper1.sv
$PRJ/./ddr4_v2_2_axi_opcode_gen1.sv
//$PRJ/./ddr4_v2_2_axi_tg_top1.sv
//$PRJ/./ddr4_v2_2_axi_wrapper1.sv
$PRJ/./ddr4_v2_2_boot_mode_gen1.sv
$PRJ/./ddr4_v2_2_custom_mode_gen1.sv
$PRJ/./ddr4_v2_2_data_gen1.sv
$PRJ/./ddr4_v2_2_prbs_mode_gen1.sv

-y ./test1/test11/test111

$PRJ./example_top1.sv
$PRJ./interface1.sv
$PRJ./MemoryArray1.sv
$PRJ./microblaze_mcs_01.sv

+incdir+/test1/test11/+
+incdir+/test1/

-v $PRJ/./ddr4_v2_2_data_chk1.sv

$PRJ./proj_package1.sv
$PRJ./sim_tb_top1.sv
$PRJ./StateTableCoe1.sv
$PRJ./StateTable1.sv
$PRJ./timing_tasks1.sv
