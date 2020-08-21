import sys


class CPU:
    def __init__(self):
        # register
        # create 8 registers
        self.reg = [0] * 8
        # ram -> Randomn Access Memory
        # dedicate 256 bytes to memory
        self.ram = [0] * 256
        # pc = Program Counter -> stores address of current instruction
        self.pc = 0

        self.reg[7] = 0xF4

        # Stack pointer
        self.sp = self.reg[7]

    # MAR = Memory Access Register -> stores mem address for read/write
    def ram_read(self, mar):
        return self.ram[mar]

    # MDR = Memory Data Register -> holds write value or value that was read
    # mar = address, mdr = value
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self, program):
        """Load a program into memory."""
        try:
            address = 0

            with open(program) as f:
                for line in f:
                    # remove '#' from lines
                    line_split = line.split("#")[0]
                    # string number
                    action = line_split.strip()

                    if action == "":
                        continue

                    # set instruction based on aciton
                    instruction = int(action, 2)
                    self.ram_write(address, instruction)

                    address += 1

        except FileExistsError:
            print("Error: File not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        # addition
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # multiplication
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def run(self):
        """Run the CPU."""

        # INSTRUCTIONS
        # halt
        HLT = 0b00000001
        # pointer
        LDI = 0b10000010
        # print
        PRN = 0b01000111

        # MATH
        # add
        ADD = 0b10100000
        # multiply
        MUL = 0b10100010

        # STACK
        # push (add to stack)
        PUSH = 0b1000101
        # pop (remove from stack)
        POP = 0b01000110

        CALL = 0b01010000

        RET = 0b00010001

        # computer "on" var to perform while loop
        isRunning = True

        while isRunning:
            # set instruction from our pc counter
            instruction = self.ram_read(self.pc)

            # standard naming convention is opr_a (operation)
            # convience variables
            opr_a = self.ram_read(self.pc + 1)
            opr_b = self.ram_read(self.pc + 2)

            # halt program turn "off" computer
            if instruction == HLT:
                self.pc += 1
                isRunning = False

            # load immediate value
            elif instruction == LDI:
                self.reg[opr_a] = opr_b
                self.pc += 3

            # case: print
            elif instruction == PRN:
                self.pc += 2
                print(self.reg[opr_a])

            # case: add
            elif instruction == ADD:
                self.alu("ADD", opr_a, opr_b)
                self.pc += 3

            # case: multiply
            elif instruction == MUL:
                self.alu("MUL", opr_a, opr_b)
                self.pc += 3

            # case: stack -> push
            elif instruction == PUSH:
                # self.ram_write(self.reg[opr_a], self.sp)
                value = self.reg[opr_a]
                self.sp -= 1
                self.ram[self.sp] = value
                self.pc += 2

            elif instruction == POP:
                # value = self.ram_read(self.sp)
                value = self.ram[self.sp]
                self.reg[opr_a] = value
                self.sp += 1
                self.pc += 2

            elif instruction == CALL:
                return_address = self.pc + 2
                self.sp -= 1
                self.ram[self.sp] = return_address
                register_store = self.ram[self.pc + 1]
                sub_routine = self.reg[register_store]
                self.pc = sub_routine

            elif instruction == RET:
                address = self.ram[self.sp]
                self.sp += 1
                self.pc = address

            else:
                # DEBUG
                print(f"self.pc = {self.pc}")
                print(f"last instruction = {self.ram_read(self.pc)}")
                isRunning = False
                sys.exit(1)

