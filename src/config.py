from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(dirname(__file__)), '.env.local')
load_dotenv(dotenv_path)

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in environment variables.")