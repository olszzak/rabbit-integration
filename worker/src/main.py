import asyncio

from clients.communicator import get_communicator


async def main() -> None:
    communicator = await get_communicator()

    await communicator.listen_for_upload_data()
    await communicator.listen_for_download_data()

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
