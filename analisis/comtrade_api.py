import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the private key
api_key = os.getenv('COMTRADE_API_KEY')

# Use the API key in your code
print(api_key)