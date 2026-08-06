from django.core.management.base import BaseCommand
import requests
import hashlib
import re

from tracker.models import Posting, Application

KEYWORD_PATTERN = re.compile(r"\bintern(s|ship|ships)?\b|\bco-?ops?\b|\bstudents?\b")

SOURCES = [
    {"ats": "greenhouse", "token": "stripe", "company": "Stripe"},
    {"ats": "greenhouse", "token": "cloudflare", "company": "Cloudflare"},
    {"ats": "greenhouse", "token": "faire", "company": "Faire"},
    {"ats": "ashby", "token": "cohere", "company": "Cohere"},
    {"ats": "ashby", "token": "1Password", "company": "1Password"},
]

def normalize_greenhouse(job, company):
    return {
        "company": company,
        "title": job["title"],
        "url": job["absolute_url"],
        "location": job["location"]["name"],
    }

def normalize_ashby(job, company):
    return {
        "company": company,
        "title": job["title"],
        "url": job["jobUrl"],
        "location": job["location"],
    }

def content_hash(posting_data):
    fingerprint = f"{posting_data["company"]}|{posting_data["title"]}|{posting_data["url"]}|{posting_data["location"]}"
    return hashlib.sha256(fingerprint.encode()).hexdigest()


class Command(BaseCommand):
    help = "Fetch job postings from sources and save the co-op/intern ones."

    def handle(self, *args, **options):
        saved_count = 0
        for source in SOURCES:
            ats = source["ats"]
            token = source["token"]
            company = source["company"]

            if ats == "greenhouse":
                url = f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs"
            elif ats == "ashby":
                url = f"https://api.ashbyhq.com/posting-api/job-board/{token}?includeCompensation=true"

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Skipping {token}: {e}"))
                continue

            for job in data["jobs"]:
                title = job["title"]
                if KEYWORD_PATTERN.search(title.lower()):
                    if ats == "greenhouse":
                        posting_data = normalize_greenhouse(job, company)
                    elif ats == "ashby":
                        posting_data = normalize_ashby(job, company)
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
