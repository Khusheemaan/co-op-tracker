import requests

def normalize(job):
    return {
        "company": job["company_name"],
        "title": job["title"],
        "url": job["absolute_url"],
        "location": job["location"]["name"],
    }

url = "https://boards-api.greenhouse.io/v1/boards/stripe/jobs"

response = requests.get(url)
data = response.json()

for job in data["jobs"]:
    title = job["title"]
    words = title.lower().split()
    if "intern" in words or "co-op" in words or "internship" in words or "coop" in words:
        posting = normalize(job)
        print(posting)