import sys
import pygame
from chip import Chip_8

args = sys.argv

pygame.init()
program_start = pygame.time.get_ticks()
screen = pygame.display.set_mode((640, 320))
font_data = "0xF0,0x90,0x90,0x90,0xF0,0x20,0x60,0x20,0x20,0x70,0xF0,0x10,0xF0,0x80,0xF0,0xF0,0x10,0xF0,0x10,0xF0,0x90,0x90,0xF0,0x10,0x10,0xF0,0x80,0xF0,0x10,0xF0,0xF0,0x80,0xF0,0x90,0xF0,0xF0,0x10,0x20,0x40,0x40,0xF0,0x90,0xF0,0x90,0xF0,0xF0,0x90,0xF0,0x10,0xF0,0xF0,0x90,0xF0,0x90,0x90,0xE0,0x90,0xE0,0x90,0xE0,0xF0,0x80,0x80,0x80,0xF0,0xE0,0x90,0x90,0x90,0xE0,0xF0,0x80,0xF0,0x80,0xF0,0xF0,0x80,0xF0,0x80,0x80"
clock = pygame.time.Clock()

if __name__ == "__main__":
    chip8 = Chip_8()
    font = font_data.split(",")
    for i in range(80):
        chip8._memory[i] = int(font[i], 16)
    with open(args[1], "rb") as rom:
        stuff = rom.read()
        for i in stuff:
            chip8._rom_data.append(i)
    for byte in chip8._rom_data:
        chip8._memory[chip8._pc] = byte
        chip8._pc += 1
    chip8._pc = 512
    running = True
    while running == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in chip8._keymap:
                chip8._key[chip8._keymap[event.key]] = 1
            elif event.type == pygame.KEYUP and event.key in chip8._keymap:
                chip8._key[chip8._keymap[event.key]] = 0
        chip8.fetch()
        chip8.execute()
        if chip8._drawFlag == True:
            screen.fill((0, 0, 0))
            for x in range(64):
                for y in range(32):
                    if chip8._display[x + (y * 64)] == 1:
                        pygame.draw.rect(screen, (255, 255, 255),
                                (x * 10, y * 10, 10, 10))
            pygame.display.flip()
            chip8._drawFlag = False
        cpu_speed = 2000
        if len(args) > 2:
            cpu_speed = int(args[2])
        chip8._timer += clock.tick(cpu_speed) / 1000
        if chip8._timer >= 1 / 60:
            if chip8._delay_timer > 0:
                chip8._delay_timer -= 1
            if chip8._sound_timer > 0:
                chip8._sound_timer -= 1
            chip8._timer = 0