/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_298a_8b_cnt (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    sync_8b_cnt u_counter (
        .clk      (clk),
        .rst_n    (rst_n),
        .ena      (ena),
        .load_ena (ui_in[0]),
        .load     (uio_in),
        .cnt_out  (uo_out)
    );

    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

endmodule
