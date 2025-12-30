"""Database models and CRUD operations for Scent Quiz System"""

from database.db_config import execute_query, execute_many

class User:
    @staticmethod
    def create(name, email, age, gender):
        query = '''
            INSERT INTO Users (name, email, age, gender)
            VALUES (%s, %s, %s, %s)
            RETURNING user_id
        '''
        result = execute_query(query, (name, email, age, gender), fetch=True)
        return result[0][0] if result else None
    
    @staticmethod
    def get_all():
        query = 'SELECT * FROM Users ORDER BY created_at DESC'
        return execute_query(query, fetch=True)
    
    @staticmethod
    def get_by_id(user_id):
        query = 'SELECT * FROM Users WHERE user_id = %s'
        return execute_query(query, (user_id,), fetch=True)
    
    @staticmethod
    def get_by_email(email):
        query = 'SELECT * FROM Users WHERE email = %s'
        return execute_query(query, (email,), fetch=True)

class ScentNote:
    @staticmethod
    def create(note_name, category):
        query = '''
            INSERT INTO ScentNotes (note_name, category)
            VALUES (%s, %s)
            RETURNING scent_note_id
        '''
        result = execute_query(query, (note_name, category), fetch=True)
        return result[0][0] if result else None
    
    @staticmethod
    def get_all():
        query = 'SELECT * FROM ScentNotes ORDER BY category, note_name'
        return execute_query(query, fetch=True)
    
    @staticmethod
    def get_by_category(category):
        query = 'SELECT * FROM ScentNotes WHERE category = %s'
        return execute_query(query, (category,), fetch=True)

class Question:
    @staticmethod
    def create(question_text, question_type):
        query = '''
            INSERT INTO Questions (question_text, question_type)
            VALUES (%s, %s)
            RETURNING question_id
        '''
        result = execute_query(query, (question_text, question_type), fetch=True)
        return result[0][0] if result else None
    
    @staticmethod
    def get_all():
        query = 'SELECT * FROM Questions ORDER BY question_id'
        return execute_query(query, fetch=True)
    
    @staticmethod
    def get_options(question_id):
        query = '''
            SELECT o.*, sn.note_name, sn.category
            FROM Options o
            LEFT JOIN ScentNotes sn ON o.scent_note_id = sn.scent_note_id
            WHERE o.question_id = %s
        '''
        return execute_query(query, (question_id,), fetch=True)

class Session:
    @staticmethod
    def create(user_id):
        query = '''
            INSERT INTO Sessions (user_id)
            VALUES (%s)
            RETURNING session_id
        '''
        result = execute_query(query, (user_id,), fetch=True)
        return result[0][0] if result else None
    
    @staticmethod
    def complete(session_id):
        query = 'UPDATE Sessions SET completed_at = CURRENT_TIMESTAMP WHERE session_id = %s'
        return execute_query(query, (session_id,))
    
    @staticmethod
    def get_by_user(user_id):
        query = '''
            SELECT * FROM Sessions 
            WHERE user_id = %s 
            ORDER BY started_at DESC
        '''
        return execute_query(query, (user_id,), fetch=True)
    
    @staticmethod
    def get_all():
        query = '''
            SELECT s.*, u.name, u.email
            FROM Sessions s
            JOIN Users u ON s.user_id = u.user_id
            ORDER BY s.started_at DESC
        '''
        return execute_query(query, fetch=True)

class Response:
    @staticmethod
    def create(session_id, question_id, option_id):
        query = '''
            INSERT INTO Responses (session_id, question_id, option_id)
            VALUES (%s, %s, %s)
            RETURNING response_id
        '''
        result = execute_query(query, (session_id, question_id, option_id), fetch=True)
        return result[0][0] if result else None
    
    @staticmethod
    def get_by_session(session_id):
        query = '''
            SELECT r.*, q.question_text, o.option_text, sn.note_name
            FROM Responses r
            JOIN Questions q ON r.question_id = q.question_id
            JOIN Options o ON r.option_id = o.option_id
            LEFT JOIN ScentNotes sn ON o.scent_note_id = sn.scent_note_id
            WHERE r.session_id = %s
            ORDER BY r.response_time
        '''
        return execute_query(query, (session_id,), fetch=True)

class ScentFormula:
    @staticmethod
    def create(session_id, base_note, middle_note, top_note):
        query = '''
            INSERT INTO ScentFormula (session_id, base_note, middle_note, top_note)
            VALUES (%s, %s, %s, %s)
            RETURNING formula_id
        '''
        result = execute_query(query, (session_id, base_note, middle_note, top_note), fetch=True)
        return result[0][0] if result else None
    
    @staticmethod
    def get_by_session(session_id):
        query = '''
            SELECT sf.*,
                   base.note_name AS base_note_name,
                   middle.note_name AS middle_note_name,
                   top.note_name AS top_note_name
            FROM ScentFormula sf
            JOIN ScentNotes base ON sf.base_note = base.scent_note_id
            JOIN ScentNotes middle ON sf.middle_note = middle.scent_note_id
            JOIN ScentNotes top ON sf.top_note = top.scent_note_id
            WHERE sf.session_id = %s
        '''
        return execute_query(query, (session_id,), fetch=True)
    
    @staticmethod
    def get_all_formulas():
        query = '''
            SELECT sf.*, u.name AS user_name,
                   base.note_name AS base_note_name,
                   middle.note_name AS middle_note_name,
                   top.note_name AS top_note_name
            FROM ScentFormula sf
            JOIN Sessions s ON sf.session_id = s.session_id
            JOIN Users u ON s.user_id = u.user_id
            JOIN ScentNotes base ON sf.base_note = base.scent_note_id
            JOIN ScentNotes middle ON sf.middle_note = middle.scent_note_id
            JOIN ScentNotes top ON sf.top_note = top.scent_note_id
            ORDER BY sf.created_at DESC
        '''
        return execute_query(query, fetch=True)

class Analytics:
    @staticmethod
    def create(user_id, session_id, total_questions, completion_time, popular_scent_note):
        query = '''
            INSERT INTO Analytics (user_id, session_id, total_questions, completion_time, popular_scent_note)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING analytics_id
        '''
        result = execute_query(query, (user_id, session_id, total_questions, completion_time, popular_scent_note), fetch=True)
        return result[0][0] if result else None
    
    @staticmethod
    def get_all():
        query = '''
            SELECT a.*, u.name AS user_name, sn.note_name AS popular_scent
            FROM Analytics a
            JOIN Users u ON a.user_id = u.user_id
            LEFT JOIN ScentNotes sn ON a.popular_scent_note = sn.scent_note_id
            ORDER BY a.created_at DESC
        '''
        return execute_query(query, fetch=True)

class Suggestion:
    @staticmethod
    def create(mood_type, description, base_note, middle_note, top_note):
        query = '''
            INSERT INTO Suggestions (mood_type, description, base_note, middle_note, top_note)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING suggestion_id
        '''
        result = execute_query(query, (mood_type, description, base_note, middle_note, top_note), fetch=True)
        return result[0][0] if result else None
    
    @staticmethod
    def get_all():
        query = '''
            SELECT s.*,
                   base.note_name AS base_note_name,
                   middle.note_name AS middle_note_name,
                   top.note_name AS top_note_name
            FROM Suggestions s
            JOIN ScentNotes base ON s.base_note = base.scent_note_id
            JOIN ScentNotes middle ON s.middle_note = middle.scent_note_id
            JOIN ScentNotes top ON s.top_note = top.scent_note_id
            ORDER BY s.mood_type
        '''
        return execute_query(query, fetch=True)
    
    @staticmethod
    def get_by_mood(mood_type):
        query = '''
            SELECT s.*,
                   base.note_name AS base_note_name,
                   middle.note_name AS middle_note_name,
                   top.note_name AS top_note_name
            FROM Suggestions s
            JOIN ScentNotes base ON s.base_note = base.scent_note_id
            JOIN ScentNotes middle ON s.middle_note = middle.scent_note_id
            JOIN ScentNotes top ON s.top_note = top.scent_note_id
            WHERE s.mood_type = %s
        '''
        return execute_query(query, (mood_type,), fetch=True)
