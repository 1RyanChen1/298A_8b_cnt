import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, FallingEdge, ReadOnly


@cocotb.test()
async def test_project(dut):

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # -------------------
    # Reset
    # -------------------
    dut.ena.value = 0
    dut.load_ena.value = 0
    dut.load.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 2)

    # Release reset away from rising edge
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    dut.ena.value = 1

    # -------------------
    # Count
    # -------------------
    for expected in range(1, 4):
        await RisingEdge(dut.clk)
        await ReadOnly()

        assert dut.cnt_out.value == expected, \
            f"Expected {expected}, got {dut.cnt_out.value}"

    # -------------------
    # Load 67
    # -------------------

    # Change inputs safely BETWEEN rising edges
    await FallingEdge(dut.clk)

    dut.load_ena.value = 1
    dut.load.value = 67

    # This rising edge performs:
    # internal_count <= load
    await RisingEdge(dut.clk)

    # Wait until Verilog finishes updating registers
    await ReadOnly()

    assert dut.cnt_out.value == 67, \
        f"Expected 67, got {dut.cnt_out.value}"

    # -------------------
    # Resume counting
    # -------------------
    await FallingEdge(dut.clk)
    dut.load_ena.value = 0

    await RisingEdge(dut.clk)
    await ReadOnly()

    assert dut.cnt_out.value == 68, \
        f"Expected 68, got {dut.cnt_out.value}"

    dut._log.info("TEST PASSED")
