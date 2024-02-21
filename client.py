import asyncio
import aiohttp


async def main():
    client = aiohttp.ClientSession()

    # response = await client.post(
    #     'http://127.0.0.1:8080/announcements/',
    #     json={
    #         'title': 'announcement_1',
    #         'description': 'first_announcement',
    #         'owner': 'Dmitrii'
    #         }
    # )
    # print(response.status)
    # print(await response.text())

    # response = await client.get(
    #     'http://127.0.0.1:8080/announcements/1/',
    # )
    # print(response.status)
    # print(await response.text())

    # response = await client.patch(
    #     'http://127.0.0.1:8080/announcements/1/',
    #     json={'title': 'user_123'}
    # )
    # print(response.status)
    # print(await response.text())

    # response = await client.get(
    #     'http://127.0.0.1:8080/announcements/1/',
    # )
    # print(response.status)
    # print(await response.text())

    # response = await client.delete(
    #     'http://127.0.0.1:8080/announcements/1/')
    # print(response.status)
    # print(await response.text())

    # response = await client.get(
    #     'http://127.0.0.1:8080/announcements/1/',
    # )
    # print(response.status)
    # print(await response.text())

    await client.close()


if __name__ == '__main__':
    asyncio.run(main())
