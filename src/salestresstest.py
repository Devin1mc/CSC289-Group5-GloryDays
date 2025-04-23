import asyncio
import aiohttp
import random
import time

# Define a function to send a POST request to the /sell endpoint
async def send_request(session, url, data=None):
    try:
        # Send a POST request with the data (e.g., item sale data) in JSON format
        async with session.post(url, json=data) as response:
            return await response.json()  # Return the JSON response from the server
    except Exception as e:
        print(f"Error during request: {e}")
        return None

# Function to generate random data for each sale request (simulates a sale)
known_skus = ['001S0G', '002X1L', '004P0O']  # Replace with real SKUs from the DB

def generate_random_data():
    return {
        "sku": random.choice(known_skus),
        "quantity": random.randint(1, 10),
        "sale_price": round(random.uniform(5.0, 100.0), 2)
    }

# Main function that performs the stress test by sending multiple requests
async def run_stress_test(url, num_requests):
    # Create an aiohttp session to manage HTTP requests
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_requests):
            data = generate_random_data()  # Generate random sale data
            task = asyncio.ensure_future(send_request(session, url, data))  # Create a task for each request
            tasks.append(task)  # Add task to list
        
        # Run all tasks concurrently and wait for their completion
        results = await asyncio.gather(*tasks)
        return results

# Main entry point for the script
if __name__ == '__main__':
    url = "http://127.0.0.1:5000/sell"  # URL to our Flask /sell endpoint (running locally)
    num_requests = 100  # The number of requests to simulate in parallel

    # Measure the start time of the stress test
    start_time = time.time()
    
    # Run the stress test
    results = asyncio.run(run_stress_test(url, num_requests))
    
    # Measure the end time after the test completes
    end_time = time.time()
    
    # Output the results
    print(f"Completed {num_requests} requests in {end_time - start_time:.2f} seconds")
    print(f"Results: {results}")  # Optionally, process and display the results
