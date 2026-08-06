from django.core.management.base import BaseCommand
import requests
import hashlib

from tracker.models import Posting, Application


def normalize(job):
    return {
        "company": job["company_name"],
        "title": job["title"],
        "url": job["absolute_url"],
        "location": job["location"]["name"],
    }

def content_hash(posting_data):
    fingerprint = f"{posting_data["company"]}|{posting_data["title"]}|{posting_data["url"]}|{posting_data["location"]}"
    return hashlib.sha256(fingerprint.encode()).hexdigest()


class Command(BaseCommand):
    help = "Fetch job postings from sources and save the co-op/intern ones."

    def handle(self, *args, **options):
        companies = ["stripe", "cloudflare", "faire"]

        saved_count = 0
        for company in companies:
            url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
            try:
                response = requests.get(url, timeout = 10)
                response.raise_for_status() #turns an http error into a catchable exception.
                data = response.json()
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Skipping {company}:{e}"))

                continue

            for job in data["jobs"]:
                title = job["title"]
                words = title.lower().split()
                if "intern" in words or "co-op" in words:
                    posting_data = normalize(job)
                    posting_hash = content_hash(posting_data)
                    if Posting.objects.filter(content_hash=posting_hash).exists():
                        continue
                    posting = Posting.objects.create(
                        company=posting_data["company"],
                        title=posting_data["title"],
                        url=posting_data["url"],
                        location=posting_data["location"],
                        content_hash=posting_hash,
                    )
                    Application.objects.create(posting=posting)
                    saved_count += 1

        self.stdout.write(self.style.SUCCESS(f"Saved {saved_count} new posting(s)."))
