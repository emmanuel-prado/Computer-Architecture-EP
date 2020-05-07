"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8  # 8 general 8 bit registers
        # ram is the computer's memory, can hold 256 bytes of RAM total
        self.ram = [0] * 256
        self.PC = 0  # address of the currently executing instruction
        self.FL = [0] * 8  # 8-bit Flags register

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, MAR):
        # MAR (Memory Address Register) contains the address being read from
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        # MAR (Memory Address Register) contains the address being written to
        # MDR (Memory Data Register) contains the data to write
        self.ram[MAR] = MDR

    def hlt(self):
        sys.exit()

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            # self.fl,
            # self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # The instruction pointed to by the PC is fetched from RAM, decoded, and executed
        while True:
            # read the memory address that's stored in register PC and store it in IR
            # IR = Instruction Register
            IR = self.ram[self.PC]
            # use ram_read() to read the bytes at PC+1 and PC+2 into variables operand_a and operand_b
            # in case the instruction needs them
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            if IR == 0b00000001:  # HLT: Halt the CPU and exit the emulator
                sys.exit()
            elif IR == 0b10000010:  # LDI: Set the value of a register to an integer
                self.reg[self.ram[self.PC + 1]] = self.ram[self.PC + 2]
                self.PC += 3
            elif IR == 0b01000111:  # PRN: Print numeric value stored in the given register
                print(self.reg[self.ram[self.PC + 1]])
                self.PC += 2

            self.PC += 1
