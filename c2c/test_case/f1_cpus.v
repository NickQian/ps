module cpus (ARREADY_p3                                                            ARID_p3[13:0]
 AWREADY_p3                                                            ARQOS_p3_final[3:0]
BID_p3[13:0]                                                               AWID_p3[13:0]
BRESP_p3[1:0]                                                           AWQOS_p3_final[3:0]
BVALID_p3                                                                 araddr_slave_0[32:0]
RDATA_p3[127:0]                                                      arburst_slave_0[1:0]
RID_p3[13:0]                                                               arlock_slave_0
RLAST_p3                                                                    arprot_slave_0[1:0]
RRESP_p3[1:0]                                                          arsize_slave_0[2:0]
RVALID_p3                                                                 arvalid_slave_0
WREADY_p3                                                          awaddr_slave_0[32:0]
WREADY_p3                                                            aw_burst_slave[1:0]
 hclk_resetn_i                                                            wdata_slave_0[127:0]
  hrdata_slave_1[31:0]                                                 wstrb_slave_0[15:0]
hreadyout_salve_1_0
hresp_slave_1_0

);


endmoudle
