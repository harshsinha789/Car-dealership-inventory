# Motor House — Car Dealership Inventory System

A full-stack inventory application built to meet the Car Dealership Inventory System kata: JWT authentication, protected vehicle management, searching/filtering, purchase and restock operations, React UI, and backend tests.

## Features
- Register and sign in using JWT access tokens.
- Browse and search vehicles by make, model, category, and price range through the API.
- Purchase stock with an atomic quantity decrement; prevents overselling.
- Staff/admin users can create, update, delete and restock vehicles.
- Persistent SQLite database for local development.
- Django admin for managing staff accounts and inventory.
- Initial backend tests for auth, permissions, and purchase behavior.

## Requirements
Python 3.10+, Node.js 20+, npm.

## Run locally
### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
API runs at `http://127.0.0.1:8000`. Register via `POST /api/auth/register`, obtain JWT via `POST /api/auth/login`, then send `Authorization: Bearer <access-token>`.

### Frontend
In another terminal:
```bash
cd frontend
npm install
npm run dev
```
Open the Vite URL (usually `http://localhost:5173`). Set `VITE_API_URL` if your backend API is hosted somewhere else.

## API overview
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/refresh`
- `GET /api/vehicles/` — authenticated list; supports `?make=Toyota&model=Corolla&category=suv&min_price=10000&max_price=50000`
- `POST /api/vehicles/` — staff only
- `GET /api/vehicles/{id}/`
- `PUT/PATCH /api/vehicles/{id}/` — staff only
- `DELETE /api/vehicles/{id}/` — staff only
- `POST /api/vehicles/{id}/purchase/` — authenticated; JSON `{ "quantity": 1 }`
- `POST /api/vehicles/{id}/restock/` — staff only; JSON `{ "quantity": 5 }`

Note: The assignment examples use paths without trailing slashes in some places; Django REST Framework's router uses trailing slashes by default.

## Tests
```bash
cd backend
pytest
```
Run frontend tests with `cd frontend && npm test` (frontend test suite should be expanded as UI features are finalized). Save the real test output in `test-report.txt` before submission. Do not claim tests passed unless you ran them locally.

## Admin setup
Create a superuser using `python manage.py createsuperuser`, then visit `/admin/`. Only staff/superusers can modify or restock inventory. Public registration creates ordinary users.

## Screenshots
Add screenshots of login, inventory, search/filter, and purchase flow here after running the application.

## My AI Usage
I used ChatGPT to help plan the architecture, scaffold boilerplate, draft backend tests, and build the initial React interface. I reviewed the generated code and should test and understand each part before submission. AI assistance helped me move faster from requirements to a working project structure, while also giving me a checklist of areas to validate, such as permissions, stock concurrency, input validation, and setup instructions. I will update this section with the actual tools and specific assistance used during development, and I will be prepared to explain the implementation in an interview.

## TDD and Git workflow
To demonstrate the required Red-Green-Refactor workflow, commit test-first changes in small steps. Example sequence:
1. `test: add registration and login tests`
2. `feat: implement JWT registration and login`
3. `test: cover stock purchase and overselling`
4. `feat: implement atomic inventory purchase`
5. `test: enforce staff-only inventory mutations`
6. `feat: restrict inventory mutations to staff`

Use the assignment's requested AI co-author trailer on commits where AI assistance was used, and use the accurate tool name/email format required by your evaluator. `PROMPTS.md` must contain actual raw logs or public chat links before submission; this starter file is only a reminder.

## Production checklist
- Replace `SECRET_KEY`; set `DEBUG=False` and configure `ALLOWED_HOSTS`.
- Use HTTPS, secure token storage, and production CORS settings.
- Configure database backups and logging.
- Add pagination, API schema, more edge-case tests, frontend tests, and screenshots.
- Run the full test suite and record the actual results.
