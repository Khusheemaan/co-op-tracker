# Co-op Application Tracker

## One-paragraph spec
A web app that helps a student run their co-op job hunt in one place. A user saves
job postings (typed in by hand at first, auto-collected later), and each saved posting
becomes an "application" they move through stages — Saved → Applied → Online Assessment
→ Interview → Offer / Rejected — with the app recording every stage change as a
timestamped history entry. The app sends reminders before deadlines and for follow-ups,
and shows simple analytics (how many applications sit in each stage, response rate). The
impressive core — added after the basic app already works — is an ingestion pipeline: a
scheduled job that pulls in new postings automatically, removes duplicates by hashing
each posting's content, and is safe to re-run, so running it twice never creates
duplicates or loses updates, and it fails gracefully when a source changes or goes down.

## Who it's for
Me — and any student running a co-op / internship search.

## Core features
1. Sign up / log in (Django's built-in auth).
2. Add a posting by hand (company, title, link, deadline) → it becomes an application in "Saved".
3. Move an application through its stages; every change is written to a history log.
4. Deadline and follow-up reminders.
5. Analytics: count by stage, response rate.
6. [THE HARD PART — added later] Scheduled ingestion that collects postings, dedupes by
   content hash, and re-runs safely (idempotent) without creating duplicates.

## Stretch goal (Phase 2 — only after the core works, and only if I can defend it)
Add an **LLM-based extraction step** inside the ingestion pipeline: feed a raw, messy job
posting to an LLM and get back clean structured fields (company, title, deadline, required
skills, and a "requires citizenship/PR" flag so I can auto-filter roles I can't take).

The point is NOT "it calls an LLM" (that part is trivial) — it's the reliability engineering
around an unreliable model, which is the defensible part:
- structured (JSON) output validated against a schema,
- a fallback path for when the model hallucinates or returns malformed data,
- caching + limiting calls to control cost (or a free local model via Ollama),
- deciding when NOT to call the LLM at all.

Why it's worth doing: it replaces the fake AI bullets on my old resume with ONE real LLM
feature I actually own — turning the AI section from a liability into an honest asset. And
LLM-as-a-pipeline-component is what "AI in everything" actually means in industry, not chatbots.

Hard rule for this feature (stricter than anywhere else): if I can't explain every decision
in it under follow-up questions, it does not ship. This is the single easiest place to let a
tool write code I don't understand — which is the exact trap I'm escaping.

## The one rule
The boring 70% (login, forms, pages) can lean on docs/tutorials/AI.
The hard 30% (the state machine + the ingestion pipeline) I build and understand myself,
because that is what the interview is about.
