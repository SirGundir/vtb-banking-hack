import asyncio

from app_instance import app


async def main():
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
