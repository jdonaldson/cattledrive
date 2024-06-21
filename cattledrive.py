import requests
import os

# Cloudflare API endpoint
# API documentation: https://api.cloudflare.com/#getting-started-endpoints
API_ENDPOINT = "https://api.cloudflare.com/client/v4/zones"

# Your Cloudflare account details
# How to find your Account ID: https://developers.cloudflare.com/fundamentals/get-started/basic-tasks/find-account-and-zone-ids/
ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID")

# How to create API tokens: https://developers.cloudflare.com/api/tokens/create/
API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN")

# List of domains
domains = [
    "dyf.io",
    "hub.apartments",
    "hub.auction",
    "hub.autos",
    "hub.boats",
    "hub.builders",
    "hub.condos",
    "hub.construction",
    "hub.contractors",
    "hub.enterprises",
    "hub.homes",
    "hub.hospital",
    "hub.lease",
    "hub.mortgage",
    "hub.rentals",
    "hub.restaurant",
    "hub.salon",
    "hub.vet",
    "jdonaldson.org",
    "jjd.io",
    "llm.fyi"
]

# Headers for API request
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def create_website(domain):
    # Step 1: Create a new zone (domain)
    # API documentation: https://api.cloudflare.com/#zone-create-zone
    zone_data = {
        "name": domain,
        "account": {"id": ACCOUNT_ID},
        "jump_start": True
    }
    response = requests.post(API_ENDPOINT, headers=headers, json=zone_data)

    if response.status_code == 200:
        zone_id = response.json()['result']['id']
        print(f"Successfully created zone for {domain}")

        # Step 2: Add a DNS record
        # API documentation: https://api.cloudflare.com/#dns-records-for-a-zone-create-dns-record
        dns_data = {
            "type": "A",
            "name": "@",
            "content": "192.0.2.1",  # Example IP, replace with your actual web server IP
            "ttl": 1,
            "proxied": True
        }
        dns_response = requests.post(f"{API_ENDPOINT}/{zone_id}/dns_records", headers=headers, json=dns_data)

        if dns_response.status_code == 200:
            print(f"Successfully added DNS record for {domain}")
        else:
            print(f"Failed to add DNS record for {domain}. Error: {dns_response.text}")
    else:
        print(f"Failed to create zone for {domain}. Error: {response.text}")

# Create websites for each domain
for domain in domains:
    create_website(domain)
