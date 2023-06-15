import connection

@connection.connection_handler
def add_user(cursor, user_name, user_password):
    from datetime import datetime
    dt = datetime.now().strftime("%Y-%m-%d %H:%M")
    role = "User"
    query = f"""
            INSERT INTO "users" (user_name, user_pass, date_reg, user_role, user_rep)
            VALUES ('{user_name}', '{user_password}', '{dt}', 'user', 0)
            RETURNING user_name"""
    cursor.execute(query, (user_name, user_password,))

@connection.connection_handler
def get_user_data_by_username(cursor, username):
    query = """
            SELECT * 
            FROM users
            WHERE user_name = %s
            """
    cursor.execute(query, (username,))
    return cursor.fetchone()