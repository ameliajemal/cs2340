# Job Board (CS2340)

## Recruiter Candidate Search

<<<<<<< HEAD
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

## Admin: Manage Users and Roles (Built-in Django Admin)

We leverage Django's admin site to fulfill the story "As an Administrator, I want to manage users and roles so the platform remains fair and safe."

### Setup default groups/roles and permissions

From `cs2340/job_board/` run:

```bash
python3 manage.py setup_roles --with-demo-admin
```

This creates groups `Regular`, `Moderator`, and `Admin` with sensible permissions and a demo superuser:
- Username: `site_admin`
- Password: `admin123`

### Access the Admin

```bash
python3 manage.py runserver
```
Visit http://127.0.0.1:8000/admin/ and log in as the demo admin (or your own superuser).

In the Users list, you can:
- Use bulk actions to deactivate/reactivate users.
- Assign group-based roles via actions: Regular, Moderator, Admin.
- View a user's `UserProfile` inline and see their `Account Role` and `Groups` columns.
=======
-  `test_recruiter / testpass123` is seeded).
-  `test_applicant / testpass123` is seeded).
>>>>>>> 3c332efe7b3bb2c54ef0b7f2f14a7c8d0f9ff9b5
