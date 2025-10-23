#!/usr/bin/env python3
"""
Script to download placeholder images for the e-commerce website
"""
import os
import requests
from urllib.parse import urljoin

# Create images directory if it doesn't exist
os.makedirs('static/images', exist_ok=True)

# Image URLs (placeholder images from Picsum)
image_urls = {
    'tshirt.jpg': 'https://picsum.photos/500/500?random=1',
    'jeans.jpg': 'https://picsum.photos/500/500?random=2',
    'shoes.jpg': 'https://picsum.photos/500/500?random=3',
    'jacket.jpg': 'https://picsum.photos/500/500?random=4',
    'hero.jpg': 'https://picsum.photos/1200/600?random=5',
    'logo.png': 'https://picsum.photos/100/100?random=6',
    'contact.jpg': 'https://picsum.photos/800/400?random=7'
}

print("Downloading placeholder images...")

for filename, url in image_urls.items():
    filepath = os.path.join('static/images', filename)

    # Skip if file already exists
    if os.path.exists(filepath):
        print(f"{filename} already exists, skipping...")
        continue

    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to download {filename}: Status code {response.status_code}")
    except Exception as e:
        print(f"Error downloading {filename}: {str(e)}")

print("Image download completed!")
