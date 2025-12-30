"""Database setup script - creates database and tables for Scent Quiz System"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Create the database if it doesn't exist"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password='0000',
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='scentdb'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute('CREATE DATABASE scentdb')
            print("Database 'scentdb' created successfully")
        else:
            print("Database 'scentdb' already exists")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def create_tables():
    """Create all required tables"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password='0000',
            database='scentdb'
        )
        cursor = conn.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
            user_id SERIAL PRIMARY KEY, name VARCHAR(100), email VARCHAR(150) UNIQUE,
            age INT, gender VARCHAR(20), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS ScentNotes (
            scent_note_id SERIAL PRIMARY KEY, note_name VARCHAR(100), category VARCHAR(100))''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS Sessions (
            session_id SERIAL PRIMARY KEY, user_id INT, started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP, FOREIGN KEY (user_id) REFERENCES Users(user_id))''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS Questions (
            question_id SERIAL PRIMARY KEY, question_text VARCHAR(255), question_type VARCHAR(50))''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS Options (
            option_id SERIAL PRIMARY KEY, question_id INT, option_text VARCHAR(255), scent_note_id INT,
            FOREIGN KEY (question_id) REFERENCES Questions(question_id),
            FOREIGN KEY (scent_note_id) REFERENCES ScentNotes(scent_note_id))''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS Responses (
            response_id SERIAL PRIMARY KEY, session_id INT, question_id INT, option_id INT,
            response_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES Sessions(session_id),
            FOREIGN KEY (question_id) REFERENCES Questions(question_id),
            FOREIGN KEY (option_id) REFERENCES Options(option_id))''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS ScentFormula (
            formula_id SERIAL PRIMARY KEY, session_id INT, base_note INT, middle_note INT, top_note INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES Sessions(session_id),
            FOREIGN KEY (base_note) REFERENCES ScentNotes(scent_note_id),
            FOREIGN KEY (middle_note) REFERENCES ScentNotes(scent_note_id),
            FOREIGN KEY (top_note) REFERENCES ScentNotes(scent_note_id))''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS Analytics (
            analytics_id SERIAL PRIMARY KEY, user_id INT, session_id INT, total_questions INT,
            completion_time INT, popular_scent_note INT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (session_id) REFERENCES Sessions(session_id),
            FOREIGN KEY (popular_scent_note) REFERENCES ScentNotes(scent_note_id))''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS Suggestions (
            suggestion_id SERIAL PRIMARY KEY, mood_type VARCHAR(50), description VARCHAR(255),
            base_note INT, middle_note INT, top_note INT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (base_note) REFERENCES ScentNotes(scent_note_id),
            FOREIGN KEY (middle_note) REFERENCES ScentNotes(scent_note_id),
            FOREIGN KEY (top_note) REFERENCES ScentNotes(scent_note_id))''')
        
        conn.commit()
        print("All tables created successfully")
        
        insert_sample_data(cursor, conn)
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

def insert_sample_data(cursor, conn):
    """Insert sample data"""
    try:
        cursor.execute("INSERT INTO Users (name, email, age, gender) VALUES ('Alice Tan', 'alice@example.com', 28, 'Female'), ('Bob Khan', 'bob@example.com', 35, 'Male'), ('Clara Lee', 'clara@example.com', 22, 'Female') ON CONFLICT (email) DO NOTHING")
        cursor.execute("INSERT INTO ScentNotes (note_name, category) VALUES ('Lavender', 'Top'), ('Vanilla', 'Middle'), ('Sandalwood', 'Base'), ('Jasmine', 'Middle'), ('Citrus', 'Top')")
        cursor.execute("INSERT INTO Questions (question_text, question_type) VALUES ('Which scent do you prefer in the morning?', 'single-choice'), ('Choose your favorite relaxing scent', 'single-choice'), ('Select scents you find energizing', 'multi-choice')")
        cursor.execute("INSERT INTO Options (question_id, option_text, scent_note_id) VALUES (1, 'Fresh Lavender', 1), (1, 'Citrus Burst', 5), (2, 'Warm Vanilla', 2), (2, 'Soothing Jasmine', 4), (3, 'Sandalwood Base', 3)")
        cursor.execute("INSERT INTO Sessions (user_id) VALUES (1), (2), (3)")
        cursor.execute("INSERT INTO Responses (session_id, question_id, option_id) VALUES (1, 1, 1), (1, 2, 3), (2, 1, 2), (2, 2, 4), (3, 3, 5)")
        cursor.execute("INSERT INTO ScentFormula (session_id, base_note, middle_note, top_note) VALUES (1, 3, 2, 1), (2, 3, 4, 5), (3, 3, 2, 5)")
        cursor.execute("INSERT INTO Analytics (user_id, session_id, total_questions, completion_time, popular_scent_note) VALUES (1, 1, 3, 120, 1), (2, 2, 3, 150, 5), (3, 3, 3, 110, 3)")
        cursor.execute("INSERT INTO Suggestions (mood_type, description, base_note, middle_note, top_note) VALUES ('Neutral', 'Balanced and calming formula', 3, 2, 1), ('Confused', 'Invigorating mix for uncertain moods', 3, 4, 5), ('Undecided', 'Gentle uplifting combination', 3, 2, 5)")
        conn.commit()
        print("Sample data inserted successfully")
    except Exception as e:
        print(f"Error inserting sample data: {e}")

if __name__ == '__main__':
    print("Starting database setup...")
    if create_database():
        create_tables()
    print("Database setup completed!")
