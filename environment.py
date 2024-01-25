import asyncio
import aiohttp
import logging

class Environment:
    has_internet = False

    @staticmethod
    async def check_internet():
        url = 'http://www.google.com/'
        timeout = aiohttp.ClientTimeout(total=5)
        try:
            logging.debug("Attempting to reach Google...")
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        Environment.has_internet = True
                        logging.debug("Internet connection successful.")
                    else:
                        Environment.has_internet = False
                        logging.debug(f"Received non-success status code: {response.status}")
        except aiohttp.ClientError as ce:
            Environment.has_internet = False
            logging.debug(f"Client error: {ce}")
        except asyncio.TimeoutError as te:
            Environment.has_internet = False
            logging.debug(f"Timeout error: {te}")

    @staticmethod
    async def start_internet_check(interval=60):
        while True:
            await Environment.check_internet()
            await asyncio.sleep(interval)

# Setup logging

# Usage
async def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    # Start checking for internet connectivity
    asyncio.create_task(Environment.start_internet_check(interval=60))

    # Example of other asynchronous tasks
    await asyncio.sleep(10)
    if Environment.has_internet:
        print("Connected to the internet.")
    else:
        print("Not connected to the internet.")

if __name__ == '__main__':
    # Run the main coroutine
    asyncio.run(main())
