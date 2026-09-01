import random
import pygame 

class Chip_8:
    def __init__(self):
        self._keymap = {pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC, pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD, pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE, pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF}
        self._rom_data= []
        self._display = bytearray(64 * 32)
        self._opcode = 0
        self._memory = bytearray(4096)
        self._I = 0
        self._pc = 512
        self._stack = []
        self._delay_timer = 0
        self._sound_timer = 0
        self._registers = [0] * 16
        self._key = [0] * 16
        self._y = 0
        self._drawFlag = False
        self._timer = 0

    def fetch(self):
        self._opcode = self._memory[self._pc] << 8 | self._memory[self._pc + 1]
        return self._opcode

    def execute(self):
        self._drawFlag = False
        str_opcode = "0x" + hex(self._opcode)[2:].zfill(4)
        if str_opcode == "0x00e0": 
            for i in range(len(self._display)):
                self._display[i] = 0
            self._drawFlag = True
        elif str_opcode == "0x00ee":
            self._pc = self._stack.pop(len(self._stack) - 1)
            return 
        elif str_opcode[2] == "a":
            self._I = self._opcode & int(str_opcode[3:], 16)
        elif str_opcode[2] == "b":
            self._pc = int(str_opcode[3:], 16) + self._registers[0]
            return 
        elif str_opcode[2] == "c":
            self._registers[int(str_opcode[3], 16)] = random.randint(0, 255) & int(str_opcode[4:], 16)
        elif str_opcode[2] == "d":
            x = (self._opcode & 0x0F00) >> 8
            y = (self._opcode & 0x00F0) >> 4
            n = (self._opcode & 0x000F)
            pixel = 0
            self._registers[15] = 0
            for i in range(n):
                pixel = self._memory[self._I + i]
                for j in range(8):
                    if ((pixel & (0x80 >> j)) != 0):
                        if self._display[((self._registers[x] + j) % 64) + (((self._registers[y] + i) % 32) * 64)] == 1:
                            self._registers[15] = 1
                        self._display[((self._registers[x] + j) % 64) + (((self._registers[y] + i) % 32) * 64)] ^= 1
            self._drawFlag = True
        elif str_opcode[2] == "e":
            if str_opcode[4:] == "9e":
                if self._key[self._registers[int(str_opcode[3], 16)]] == 1:
                    self._pc += 2
            elif str_opcode[4:] == "a1":
                if self._key[self._registers[int(str_opcode[3], 16)]] == 0:
                    self._pc += 2
        elif str_opcode[2] == "f":
            if str_opcode[4:] == "07":
                self._registers[int(str_opcode[3], 16)] = self._delay_timer
            elif str_opcode[4:] == "15":
                self._delay_timer = self._registers[int(str_opcode[3], 16)]
            elif str_opcode[4:] == "18":
                self._sound_timer = self._registers[int(str_opcode[3], 16)]
            elif str_opcode[4:] == "1e":
                self._I += self._registers[int(str_opcode[3], 16)]
            elif str_opcode[4:] == "29":
                self._I = (self._registers[int(str_opcode[3], 16)] & 0xF) * 5
            elif str_opcode[4:] == "33":
                self._memory[self._I] = self._registers[int(str_opcode[3], 16)] // 100
                self._memory[self._I + 1] = (self._registers[int(str_opcode[3], 16)] // 10) % 10
                self._memory[self._I + 2] = self._registers[int(str_opcode[3], 16)] % 10
            elif str_opcode[4:] == "55":
                for i in range(int(str_opcode[3], 16) + 1):
                    self._memory[self._I + i] = self._registers[i]
            elif str_opcode[4:] == "65":
                for i in range(int(str_opcode[3], 16) + 1):
                    self._registers[i] = self._memory[self._I + i]
            elif str_opcode[4:] == "0a":
                for i in range(16):
                    if self._key[i] == 1:
                        self._registers[int(str_opcode[3], 16)] = i
                        self._pc += 2
                        return 
                return
        elif str_opcode[2] == "1":
            self._pc = int(str_opcode[3:], 16)
            return 
        elif str_opcode[2] == "2":
            self._stack.append(self._pc + 2)
            self._pc = int(str_opcode[3:], 16)
            return
        elif str_opcode[2] == "3":
            if (self._registers[int(str_opcode[3], 16)] == int(str_opcode[4:], 16)):
                self._pc += 2
        elif str_opcode[2] == "4":
            if (self._registers[int(str_opcode[3], 16)] != int(str_opcode[4:], 16)):
                self._pc += 2
        elif str_opcode[2] == "5":
            if (self._registers[int(str_opcode[3], 16)] == self._registers[int(str_opcode[4], 16)]):
                self._pc += 2
        elif str_opcode[2] == "6":
            self._registers[int(str_opcode[3], 16)] = int(str_opcode[4:], 16)
        elif str_opcode[2] == "7":
            self._registers[int(str_opcode[3], 16)] += int(str_opcode[4:], 16)
            if self._registers[int(str_opcode[3], 16)] > 255:
                self._registers[int(str_opcode[3], 16)] = self._registers[int(str_opcode[3], 16)] - 256
        elif str_opcode[2] == "8":
            if str_opcode[5] == "0":
                self._registers[int(str_opcode[3], 16)] = self._registers[int(str_opcode[4], 16)]
            elif str_opcode[5] == "1":
                self._registers[int(str_opcode[3], 16)] = (self._registers[int(str_opcode[3], 16)] | self._registers[int(str_opcode[4], 16)])
            elif str_opcode[5] == "2":
                self._registers[int(str_opcode[3], 16)] = (self._registers[int(str_opcode[3], 16)] & self._registers[int(str_opcode[4], 16)])
            elif str_opcode[5] == "3":
                self._registers[int(str_opcode[3], 16)] = (self._registers[int(str_opcode[3], 16)] ^ self._registers[int(str_opcode[4], 16)])
            elif str_opcode[5] == "4":
                self._registers[int(str_opcode[3], 16)] = self._registers[int(str_opcode[3], 16)] + self._registers[int(str_opcode[4], 16)]
                if self._registers[int(str_opcode[3], 16)] > 255:
                    self._registers[int(str_opcode[3], 16)] -= 256
                    self._registers[15] = 1
                else:
                    self._registers[15] = 0
            elif str_opcode[5] == "5":
                if (self._registers[int(str_opcode[3], 16)] >= self._registers[int(str_opcode[4], 16)]):
                    self._registers[15] = 1
                else:
                    self._registers[15] = 0
                self._registers[int(str_opcode[3], 16)] = self._registers[int(str_opcode[3], 16)] - self._registers[int(str_opcode[4], 16)]
                if self._registers[int(str_opcode[3], 16)] < 0:
                    self._registers[int(str_opcode[3], 16)] += 256
            elif str_opcode[5] == "6":
                dropped_bit = self._registers[int(str_opcode[3], 16)] % 2
                self._registers[int(str_opcode[3], 16)] = self._registers[int(str_opcode[3], 16)] // 2
                self._registers[15] = dropped_bit
            elif str_opcode[5] == "7":
                if self._registers[int(str_opcode[4], 16)] >= self._registers[int(str_opcode[3], 16)]:
                    self._registers[15] = 1
                else:
                    self._registers[15] = 0
                self._registers[int(str_opcode[3], 16)] = (self._registers[int(str_opcode[4], 16)] - self._registers[int(str_opcode[3], 16)])
                if self._registers[int(str_opcode[3], 16)] < 0:
                    self._registers[int(str_opcode[3], 16)] += 256
            elif str_opcode[5] == "e":
                dropped_bit = self._registers[int(str_opcode[3], 16)] // 128
                self._registers[int(str_opcode[3], 16)] = (self._registers[int(str_opcode[3], 16)] * 2) % 256
                self._registers[15] = dropped_bit
        elif str_opcode[2] == "9":
            if (self._registers[int(str_opcode[3], 16)] != self._registers[int(str_opcode[4], 16)]):
                self._pc += 2
        self._pc += 2