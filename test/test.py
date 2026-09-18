import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, FallingEdge, ReadOnly


def set_bit(value, bit, bit_value):
    """Set/clear one bit in an integer."""
    if bit_value:
        return value | (1 << bit)
    else:
        return value & ~(1 << bit)


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start 8-bit counter test")

    # 100 kHz clock
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # -----------------------------
    # Initial values
    # -----------------------------
    dut.ena.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    # -----------------------------
    # Reset
    # -----------------------------
    await ClockCycles(dut.clk, 2)

    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    dut.ena.value = 1

    # load_ena = 0
    ui = int(dut.ui_in.value)
    ui = set_bit(ui, 0, 0)
    dut.ui_in.value = ui

    # -----------------------------
    # Count to 3
    # -----------------------------
    await RisingEdge(dut.clk)
    await ReadOnly()
    assert int(dut.uo_out.value) == 1, \
        f"Expected 1, got {dut.uo_out.value}"

    await FallingEdge(dut.clk)

    await RisingEdge(dut.clk)
    await ReadOnly()
    assert int(dut.uo_out.value) == 2, \
        f"Expected 2, got {dut.uo_out.value}"

    await FallingEdge(dut.clk)

    await RisingEdge(dut.clk)
    await ReadOnly()
    assert int(dut.uo_out.value) == 3, \
        f"Expected 3, got {dut.uo_out.value}"

    # -----------------------------
    # Load 67
    # -----------------------------
    await FallingEdge(dut.clk)

    dut.uio_in.value = 67

    ui = int(dut.ui_in.value)
    ui = set_bit(ui, 0, 1)     # load_ena = 1
    dut.ui_in.value = ui

    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.uo_out.value) == 67, \
        f"Expected 67, got {dut.uo_out.value}"

    # -----------------------------
    # Disable load, resume counting
    # -----------------------------
    await FallingEdge(dut.clk)

    ui = int(dut.ui_in.value)
    ui = set_bit(ui, 0, 0)     # load_ena = 0
    dut.ui_in.value = ui

    await RisingEdge(dut.clk)
    await ReadOnly()

    assert int(dut.uo_out.value) == 68, \
        f"Expected 68, got {dut.uo_out.value}"

    dut._log.info("TEST PASSED")
