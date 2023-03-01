import asyncio


async def hello():
    print("Hello ...")
    await asyncio.sleep(1)
    print("... World!")


async def main():
    await asyncio.sleep(3)
    await asyncio.gather(hello(), hello())


asyncio.run(main())
