import asyncio
import aiohttp
import time

# Function to send a GET request to the inventory data endpoint
async def send_request(session, url):
    try:
        # Send a GET request to fetch inventory data
        async with session.get(url) as response:
            # Return the response 
            return await response.json()
    except Exception as e:
        print(f"Error during request: {e}")
        return None

# Function to run stress test by sending multiple requests to the inventory endpoint
async def run_stress_test(url, num_requests):
    # Create an aiohttp session
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_requests):
            # Create an asyncio task for each request
            task = asyncio.ensure_future(send_request(session, url))
            tasks.append(task)
        
        # Run all tasks concurrently and wait for their completion
        results = await asyncio.gather(*tasks)
        return results

# Main entry point for the script
if __name__ == '__main__':
    url = "http://127.0.0.1:5000/inventory_data"  
    num_requests = 100  # The number of requests to send in parallel (adjust as needed)
    
    # Measure the start time
    start_time = time.time()
    
    # Run the stress test
    results = asyncio.run(run_stress_test(url, num_requests))
    
    # Measure the end time
    end_time = time.time()
    
    # Output the results
    print(f"Completed {num_requests} requests in {end_time - start_time:.2f} seconds")
    print(f"Results: {results}")  # Optionally process the results if needed
