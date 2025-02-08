from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve sensitive information from environment variables
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
