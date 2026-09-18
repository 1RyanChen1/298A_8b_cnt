module sync_8b_cnt(
  input wire clk,
  input wire rst_n,
  input wire ena,
  input wire load_ena,
  input wire [7:0] load,

  output reg [7:0] cnt_out
);
  reg [7:0] internal_count;
  assign cnt_out = ena ? internal_count : 8'bZ;
  
  always@(posedge clk or negedge rst_n) begin

    if(!rst_n) begin
        internal_count <= '0;
    end else begin
      if (load_ena) 
          internal_count <= load;
      else
        internal_count <= internal_count + 1;
    end
  end
endmodule
