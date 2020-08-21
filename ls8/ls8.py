#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

# pass in the program to load() to test
cpu.load(sys.argv[1])
# IndexError: list index out of range?

cpu.run()
