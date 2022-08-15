module fpga_top  # (  parameter xxx = 8, 
                      parameter yyy = 8 )     
(
 input in_a,
 input [9:0]in_BUS_A,
 output [7:0] out_bus, 
 output [xxx-1 : 0] out_c 
);


   assign [3:0] axi_awid_stpu = 5;
   
`ifdef SOME_DEFINE_MICRO_NEST_1
   assign axi_awlen_stpu = 1;
    `ifdef SOME_DEFINE_MICRO_NEST_2
       wire internal_wire1_stpu;
       wire [zzz-1:0]internal_bus1_stpu;
	`endif
`endif



ip1 u_ip1 #()(
	.axi_awid( axi_awid_stpu),
	`ifdef SOME_DEFINE_MICRO
	   .axi_awlen( axi_awlen_stpu ),	
	   .internal_wire( internal_wire1_stpu),
	`endif
	.internal_bus(internal_bus1_stpu),
	
	.in_a( in_a ),
	.inA (in_BUS_A),
	.out_bus(out_bus)
	.out_c ( out_c )
);

ip2 u_ip2 #()(

);

endmodule
