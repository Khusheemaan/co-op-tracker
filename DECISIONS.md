# Decision Log

One line per real decision I make while building this. This file IS my interview prep —
every entry is an answer to "why did you...?" or "tell me about a time you..." Keep it
honest and in my own words.

- Chose **Django** over Next.js because I'm still learning: Django gives me the database
  layer, user login, and an admin panel out of the box, so there are fewer separate tools
  to learn — and this project's hard part (scraping + scheduled jobs) is Python's strength.
- Chose **SQLite** for local development (zero setup, it's just a file on disk) and will
  switch to **PostgreSQL** at deploy time, because Postgres handles real concurrent traffic
  and is what a hosted app needs.

<!-- Add the next decision here as you build. Examples of things worth logging:
     "chose X over Y because...", "this broke when..., I fixed it by...",
     "the tradeoff I made here was..." -->

- Used a single Django app called 'tracker' to keep all my models in one place, since the project is small.
  "python manage.py startapp tracker"

- So the user types in every job by hand? Isn't that tedious?
  Answer : It would be, which is why the core feature is an ingestion pipeline that pulls postings in automatically and dedupes them. I built manual entry first because I needed the data model working before I could build something to feed it, and it's still useful as a fallback. The whole design goal was to make capturing a posting near-zero-effort.

- Explain the project
  Answer : Built a full-stack application tracker (Django/PostgreSQL) with an idempotent ingestion pipeline that deduplicates postings by content hash and re-runs safely; a state machine enforcing legal status transitions with a full audit trail; and scheduled reminders that persist across restarts.

- Explain the reason as to why you built your own application page when django's admin already built it.
  Answer : the page built by djano's admin shows generic rows in a generic tabel, if i made it available to the users, it would be dangerous as it is easily editable. So i built another applications page by myself using views, templates, URL routing and database queries, which is supposed to be the storefront for the users.
  And you literally cannot ship the Django admin to real users: it's locked behind a superuser login, it exposes every raw database field, and it can delete or edit anything with one click.

- What's a state machine?
  Answer : It's a way of modeling something that's always in exactly one of a fixed
  set of states, and moves between them through defined transitions, where
  not every move is allowed.
  Example : a traffic light, green->yellow->red->green
  a package, ordered->shipped->out for delivery-> delivered->shipped

- Walk me through your state machine, which transitions are legal, and how do you enforce that?
  Answer :

- What is StatusEvent for?
  Answer : It's an immutable log, a permanent record where every time an
  application's status changes, you write one row saying: this application went from X to Y at this time. That's your audit trail, and it's the concrete thing behind the interview answer "how do you track an application's history?" — you don't guess, you have a dated log of every
  move.

- Update Week 3:
  Built a state machine that enforces legal transitions and auto-logs every change to a StatusEvent history table.
