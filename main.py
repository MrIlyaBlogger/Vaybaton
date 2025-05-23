import pygame
import asyncio
from mechanic import Game

async def main():
    game = Game()
    await game.run_web()

def init():
    asyncio.run(main())

if __name__ == "__main__":
    init()