# Digital Scent Generator

A Python desktop application for creating personalized scent profiles through an interactive quiz system.

## Features

- 👤 **User Management** - Register and manage user profiles
- 🧪 **Interactive Quiz** - Answer questions to determine scent preferences
- 🌸 **Scent Formulas** - Generate personalized scent combinations
- 📊 **Analytics** - Track quiz completion and popular scents
- 🗑️ **Admin Panel** - Manage users and delete data

## Prerequisites

Before setting up this project, ensure you have:

- **Python 3.11+** installed
- **PostgreSQL 15+** installed and running
- **Git** installed (for version control)
- **VS Code** (recommended editor)

## Setup Instructions (New Laptop)

### Step 1: Install PostgreSQL

1. Download and install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/)
2. During installation, set the password for `postgres` user to `0000` (or update `database/db_config.py` with your password)
3. Default port should be `5432`
4. Install pgAdmin (usually included with PostgreSQL)

### Step 2: Clone the Repository

```bash
cd Desktop
git clone https://github.com/tanzeelrida21-dotcom/digitalscentgenerator.git
cd digitalscentgenerator
```

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\Activate.ps1
# Or if PowerShell doesn't allow:
.venv\Scripts\activate.bat
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Database Connection

Open `database/db_config.py` and verify/update these settings:

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': '0000',  # Change if you used different password
    'database': 'scentdb'
}
```

### Step 6: Initialize Database

Run the database setup script:

```bash
python database/db_setup.py
```

This will:
- Create the `scentdb` database
- Create all required tables (Users, Sessions, Questions, Options, Responses, ScentNotes, ScentFormula, Analytics, Suggestions)
- Insert sample quiz questions and scent notes

### Step 7: Run the Application

```bash
python main.py
```

The application window should open. You can now:
1. Register a new user or select existing user
2. Take the scent quiz
3. View your personalized scent formula
4. Check analytics and manage users

## Project Structure

```
digitalscentgenerator/
├── database/
│   ├── db_config.py          # Database connection configuration
│   ├── db_setup.py           # Database initialization script
│   └── scent_models.py       # Database models (CRUD operations)
├── frontend/
│   ├── user_entry_window.py  # User registration/login
│   ├── scent_main_window.py  # Main application window
│   ├── quiz_tab.py           # Quiz interface
│   ├── results_tab.py        # View quiz results
│   ├── formulas_tab.py       # View scent formulas
│   ├── analytics_tab.py      # Analytics dashboard
│   └── users_management_tab.py  # User management
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Database Schema

The application uses 9 tables:

1. **Users** - User profiles (name, email, age, gender)
2. **Sessions** - Quiz sessions for each user
3. **Questions** - Quiz questions
4. **Options** - Answer options for questions
5. **Responses** - User answers to questions
6. **ScentNotes** - Available scent notes (top, middle, base)
7. **ScentFormula** - Generated scent combinations
8. **Analytics** - Quiz completion statistics
9. **Suggestions** - Personalized recommendations

## Troubleshooting

### PostgreSQL Connection Error

```
Error: could not connect to server
```

**Solution:**
- Verify PostgreSQL service is running
- Check password in `db_config.py` matches your PostgreSQL password
- Ensure port 5432 is not blocked by firewall

### Database Already Exists Error

```
Error: database "scentdb" already exists
```

**Solution:**
- This is normal if you've run setup before
- The script will skip database creation and create tables
- To start fresh, drop the database in pgAdmin and run setup again

### Virtual Environment Activation Error (Windows)

```
cannot be loaded because running scripts is disabled
```

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Module Not Found Error

```
ModuleNotFoundError: No module named 'psycopg2'
```

**Solution:**
- Ensure virtual environment is activated (you should see `(.venv)` in terminal)
- Run: `pip install -r requirements.txt`

## Dependencies

- **psycopg2-binary** (2.9.9) - PostgreSQL database adapter for Python
- **tkinter** (Built-in with Python) - GUI framework

## Development

### Adding New Questions

1. Open pgAdmin and connect to `scentdb`
2. Add questions to the `Questions` table
3. Add corresponding options to the `Options` table
4. Restart the application

### Modifying Scent Notes

1. Edit the `ScentNotes` table in pgAdmin
2. Update note categories (Top, Middle, Base)
3. The quiz will automatically use the new notes

## Contributing

1. Create a new branch: `git checkout -b feature-name`
2. Make your changes
3. Commit: `git commit -m "Description"`
4. Push: `git push origin feature-name`
5. Create a Pull Request

## License

This project is for educational purposes.

## Contact

For questions or issues, please contact the development team.
