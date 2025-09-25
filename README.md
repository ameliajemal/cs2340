# Job Board (CS2340)

## Recruiter Candidate Search

This project now supports a recruiter-facing candidate search that filters by:

- Skills (multi-select)
- Location (free text match like "Atlanta" or "Remote")
- Project keywords (searches candidate project names and descriptions)

### How to run locally

1. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt  # if available
   ```

2. Apply migrations:
   ```bash
   cd job_board
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

3. Seed sample users and candidates (optional, for demo):
   ```bash
   python3 manage.py create_test_users
   python3 manage.py seed_candidates
   ```

4. Run the server:
   ```bash
   python3 manage.py runserver
   ```

### Using the feature

- Log in as a recruiter (e.g., `test_recruiter / testpass123` if seeded).
- Click the `Candidates` link in the navbar.
- Use the filters (skills, location, project keywords) and click Search.

### Notes

- Candidate data lives in the `profiles` app. We added `Profile.location` and a new `Project` model to support project-based search.
- Only users with role `recruiter` (from `accounts.UserProfile`) can access the search page.