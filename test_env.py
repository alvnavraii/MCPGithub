from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).parent / '.env'
print(f"Looking for .env at: {env_path}")
print(f"File exists: {env_path.exists()}")
print(f"File is readable: {os.access(env_path, os.R_OK)}")

if env_path.exists():
    with open(env_path, 'r') as f:
        print("\nFile contents:")
        for line in f:
            if 'TOKEN' in line:
                print("[TOKEN LINE HIDDEN]")
            else:
                print(line.strip())

load_dotenv(env_path)
token = os.getenv('GITHUB_TOKEN')
print(f"\nGITHUB_TOKEN loaded: {'Yes' if token else 'No'}")

if token:
    print("Token length:", len(token))