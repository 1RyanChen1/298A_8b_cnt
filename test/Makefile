# SPDX-License-Identifier: Apache-2.0

SIM ?= icarus
TOPLEVEL_LANG ?= verilog

SRC_DIR := $(PWD)/../src

PROJECT_SOURCES := sync_8b_cnt.v


ifneq ($(GATES),yes)

# -------------------------
# RTL simulation
# -------------------------

SIM_BUILD := sim_build/rtl

VERILOG_SOURCES += $(addprefix $(SRC_DIR)/,$(PROJECT_SOURCES))

else

# -------------------------
# Gate-level simulation
# -------------------------

SIM_BUILD := sim_build/gl

COMPILE_ARGS += -DGL_TEST
COMPILE_ARGS += -DFUNCTIONAL
COMPILE_ARGS += -DUSE_POWER_PINS
COMPILE_ARGS += -DSIM
COMPILE_ARGS += -DUNIT_DELAY=\#1

VERILOG_SOURCES += $(PDK_ROOT)/gf180mcuD/libs.ref/gf180mcu_fd_sc_mcu7t5v0/verilog/primitives.v
VERILOG_SOURCES += $(PDK_ROOT)/gf180mcuD/libs.ref/gf180mcu_fd_sc_mcu7t5v0/verilog/gf180mcu_fd_sc_mcu7t5v0.v

VERILOG_SOURCES += $(PWD)/gate_level_netlist.v

endif


# Allow Verilog `include files from src/
COMPILE_ARGS += -I$(SRC_DIR)

# Verilog module name
TOPLEVEL := sync_8b_cnt

# test/test.py
COCOTB_TEST_MODULES := test

# FST waveform for Icarus
ifeq ($(SIM),icarus)
    SIM_ARGS += -fst
endif


include $(shell cocotb-config --makefiles)/Makefile.sim
