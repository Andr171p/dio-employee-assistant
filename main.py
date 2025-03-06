import logging
import asyncio

from src.presentation import run_bot


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    await run_bot()


if __name__ == '__main__':
    asyncio.run(main())
