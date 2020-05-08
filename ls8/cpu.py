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
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    if line == "\n":
                        continue
                    else:
                        line_split = line.split("#")
                        string = line_split[0].strip()
                        instruction = int(string, 2)
                        self.ram[address] = instruction
                        address += 1
        except:
            raise ValueError("Please load a valid program")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            value = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = value
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
        HLT = 0b00000001  # Halt the CPU and exit the emulator
        LDI = 0b10000010  # Set the value of a register to an integer
        PRN = 0b01000111  # Print numeric value stored in the given register
        # ALU Ops
        ADD = 0b10100000  # Add the value in two registers and store the result in registerA
        # Multiply the values in two registers together and store the result in registerA
        MUL = 0b10100010
        while True:
            self.trace()
            # The instruction pointed to by the PC is fetched from RAM, decoded, and executed
            # IR = Instruction Register
            IR = self.ram[self.PC]
            # use ram_read() to read the bytes at PC+1 and PC+2 into variables operand_a and operand_b
            # in case the instruction needs them
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            if IR == HLT:
                sys.exit(0)
            elif IR == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.PC += 3
            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.PC += 3
            elif IR == LDI:
                address = operand_a
                integer = operand_b
                self.reg[address] = integer
                self.PC += 3
            elif IR == PRN:
                address = operand_a
                print(self.reg[address])
                self.PC += 2
