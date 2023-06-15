import connection
import os
from psycopg2.extras import RealDictCursor

DIR_PATH = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(DIR_PATH, 'static/uploads')

@connection.connection_handler
def display_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    question = cursor.fetchall()
    return question

@connection.connection_handler
def list_questions(cursor, order_by, order):
    cursor.execute(f"""
                    SELECT * FROM question 
                    ORDER BY {order_by} {order};
                    """)
    questions = cursor.fetchall()
    return questions



@connection.connection_handler
def get_answers_for_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(question_id)s
                    ORDER BY vote_number DESC;
                    """,
                   {'question_id': question_id})
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def get_answer_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT submission_time, vote_number, message FROM answer
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})

    answer = cursor.fetchall()
    return answer


@connection.connection_handler
def route_edit_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})

    question_to_edit = cursor.fetchall()
    return question_to_edit[0]


@connection.connection_handler
def edit_question(cursor, question_id, edited_title, edited_message):
    cursor.execute("""
                    UPDATE question
                    SET title = %(edited_title)s, message = %(edited_message)s
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id,
                    'edited_title': edited_title,
                    'edited_message': edited_message})


@connection.connection_handler
def increase_view_number(cursor, question_id):
    cursor.execute("""
                   UPDATE question
                   SET view_number = view_number + 1
                   WHERE id = %(question_id)s;
                   """,
                   {'question_id': question_id})


@connection.connection_handler
def add_new_data_to_table(cursor, dict, type):
    from datetime import datetime
    dt = datetime.now().strftime("%Y-%m-%d %H:%M")

    if type == "question":
        cursor.execute("""
                        INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
                        VALUES( %(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s);
                         """,
                       {'submission_time': dt,
                        'view_number': dict['view_number'],
                        'vote_number': dict['vote_number'],
                        'title': dict['title'],
                        'message': dict['message'],
                        'image': dict['image']})

    elif type == "answer":
        cursor.execute("""
                        INSERT INTO answer(submission_time, vote_number, question_id, message, image)
                        VALUES(%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s);
                        """,
                       {
                        'submission_time': dt,
                        'vote_number': dict['vote_number'],
                        'question_id': dict['question_id'],
                        'message': dict['message'],
                        'image': dict['image']})

    elif type == "comment":
        cursor.execute("""
                        INSERT INTO comment(question_id, answer_id, message, submission_time, edited_count)
                        VALUES(%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s);
                        """,
                       {
                        'question_id': dict['question_id'],
                        'answer_id': dict['answer_id'],
                        'message': dict['message'],
                        'submission_time': dt,
                        'edited_count': dict['edited_count']})


@connection.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                DELETE FROM comment
                WHERE answer_id = %(answer_id)s;
                DELETE FROM answer
                WHERE id = %(answer_id)s;
                """,
                   {'answer_id': answer_id})


@connection.connection_handler
def get_question_vote_number(cursor, question_id):
    cursor.execute("""
                    SELECT vote_number FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    vote_number = cursor.fetchall()
    return vote_number[0]


@connection.connection_handler
def update_question_vote_number(cursor, question_id, vote_number):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = %(vote_number)s
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id,
                    'vote_number': vote_number})


@connection.connection_handler
def get_answer_vote_number(cursor, question_id, answer_id):
    cursor.execute("""
                    SELECT vote_number FROM answer
                    WHERE question_id = %(question_id)s AND id = %(answer_id)s;
                    """,
                   {'question_id': question_id,
                    'answer_id': answer_id})
    vote_number = cursor.fetchall()
    return vote_number[0]


@connection.connection_handler
def update_answer_vote_number(cursor, question_id, answer_id, vote_number):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = %(vote_number)s
                    WHERE question_id = %(question_id)s AND id = %(answer_id)s;
                    """,
                   {'question_id': question_id,
                    'answer_id': answer_id,
                    'vote_number': vote_number})


@connection.connection_handler
def get_answer_for_question_by_id(cursor, answer_id, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(answer_id)s AND question_id = %(question_id)s;
                    """,
                   {'answer_id': answer_id, 'question_id': question_id})
    question_answers_data = cursor.fetchall()
    return question_answers_data


@connection.connection_handler
def update_question_answer(cursor, dict):
    cursor.execute("""
                    UPDATE answer
                    SET message = %(message)s, image = %(image)s
                    WHERE id = %(answer_id)s AND question_id = %(question_id)s;
                    """,
                   {'answer_id': dict['id'],
                    'question_id': dict['question_id'],
                    'message': dict['message'],
                    'image': dict['image']})


@connection.connection_handler
def get_last_five_question_by_time(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time DESC
                    LIMIT 5;
                    """)
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                   DELETE FROM comment
                   WHERE question_id = %(question_id)s;
                   DELETE FROM answer
                   WHERE question_id = %(question_id)s;
                   DELETE FROM question_tag
                   WHERE question_id = %(question_id)s;
                   DELETE FROM question
                   WHERE id = %(question_id)s;
                   """,
                   {'question_id': question_id})


@connection.connection_handler
def get_comments_for_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def get_comments_for_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE answer_id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def get_all_comments(cursor):
    cursor.execute("""
                    SELECT * FROM comment;
                    """)

    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(comment_id)s;
                    """,
                   {'comment_id': comment_id})


@connection.connection_handler
def route_edit_comment(cursor, comment_id):
    cursor.execute("""
                    SELECT message, submission_time, edited_count FROM comment
                    WHERE id = %(comment_id)s;
                    """,
                   {'comment_id': comment_id})
    comment_to_edit = cursor.fetchall()
    return comment_to_edit


@connection.connection_handler
def edit_comment(cursor, comment_id, message):
    from datetime import datetime
    dt = datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute("""
                    UPDATE comment
                    SET submission_time = %(submission_time)s, message = %(message)s, edited_count = edited_count + 1
                    WHERE id = %(comment_id)s;
                    """,
                   {'comment_id': comment_id,
                    'message': message,
                    'submission_time': dt})

#SEARCH

@connection.connection_handler
def get_questions(cursor, order_by='submission_time', order='desc'):
    query = f"""
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        ORDER BY {order_by} {order};"""
    cursor.execute(query)
    return cursor.fetchall()

@connection.connection_handler
def search_question(cursor, search_word):
    query = f"""
    SELECT *
    FROM question
    WHERE title ILIKE %s
    OR question.message ILIKE %s"""
    args = ['%' + search_word + '%'] * 2
    cursor.execute(query, args)
    return cursor.fetchall()

#TAGS AND STATS

@connection.connection_handler
def add_new_tag(cursor, tag_id):
    """ add new record to question_tag"""
    query =f"""
            INSERT INTO question_tag VALUES ((SELECT MAX(id) FROM question), {tag_id})
            """
    cursor.execute(query)

@connection.connection_handler
def search_by_tags(cursor, search_tag):
    """search question by tags"""
    query =f"""
        select * from question JOIN question_tag 
        ON question_tag.question_id = question.id
        WHERE tag_id = {search_tag};
        """
    cursor.execute(query)
    return cursor.fetchall()

@connection.connection_handler
def delete_tag(cursor, question_id):
    """ delete tag from database"""
    query = f"""
            DELETE from question_tag WHERE question_id={question_id};
            """
    cursor.execute(query)

@connection.connection_handler
def show_tag(cursor, question_id):
    """show questions's tag"""
    query =f"""
            SELECT name FROM tag WHERE id=
            (SELECT tag_id FROM question_tag
			WHERE question_id={question_id});
            """
    cursor.execute(query)
    return cursor.fetchone()

@connection.connection_handler
def count_tags(cursor, tag_id):
    """count how many questions are in each tag """
    query = f"""
            SELECT COUNT (tag_id) FROM question_tag
            WHERE tag_id={tag_id};
            """
    cursor.execute(query)
    return cursor.fetchone()

@connection.connection_handler
def count_users(cursor):
    """ count all registered users"""
    query = f"""
            SELECT COUNT (user_id) FROM users
            """
    cursor.execute(query)
    return cursor.fetchone()

    
#USERS AND LOGIN
@connection.connection_handler
def get_answer(cursor, answer_id):
    cursor.execute(f"""
                    SELECT * FROM answer
                    WHERE id = {answer_id}
                    """)
    return cursor.fetchall()

@connection.connection_handler
def mark_answered(cursor, answer_id, question_id):
    cursor.execute(f"""
            UPDATE answer
            SET accepted = FALSE 
            WHERE answer.question_id = {question_id}
            """)

    cursor.execute(f"""
            UPDATE answer
            SET accepted = TRUE 
            WHERE id={answer_id}""")


@connection.connection_handler
def unmark_answered(cursor, answer_id, question_id):
    cursor.execute(f"""
            UPDATE answer
            SET accepted = FALSE 
            WHERE answer.question_id = {question_id}
            """)

@connection.connection_handler
def get_user(cursor, user_id):
    cursor.execute(f"""
                    SELECT user_name, date_reg, user_rep 
                    FROM users
                    WHERE user_id={user_id}
                    """)
    return cursor.fetchall()


@connection.connection_handler
def get_user_questions(cursor, user_id):
    cursor.execute(f"""
                    SELECT id, submission_time,title FROM question q 
                    LEFT JOIN user_question u ON q.id=u.question_id WHERE u.user_id={user_id};
                    """)
    return cursor.fetchall()


@connection.connection_handler
def get_user_answers(cursor, user_id):
    cursor.execute(f"""
                    SELECT id, submission_time, message FROM answer a 
                    LEFT JOIN user_answer u ON a.id=u.answer_id WHERE u.user_id={user_id};
                    """)
    return cursor.fetchall()


@connection.connection_handler
def get_user_comments(cursor, user_id):
    cursor.execute(f"""
                    SELECT message, submission_time FROM comment c LEFT JOIN 
                    user_comment u ON c.id=u.comment_id WHERE u.user_id={user_id};
                    """)
    return cursor.fetchall()

@connection.connection_handler
def users_data(cursor: RealDictCursor):
    cursor.execute("""
              SELECT u.user_id, u.user_name, u.date_reg, 
                          count(q.user_id) AS count_question,
                            count(a.user_id) AS count_answer,
                            count(c.user_id) AS count_comment,
                            u.user_rep
                        FROM users u
                        LEFT JOIN user_question q ON u.user_id = q.user_id
                       LEFT JOIN user_answer a ON u.user_id = a.user_id
                        LEFT JOIN user_comment c ON u.user_id = c.user_id
                        GROUP BY u.user_id;
                    """)
    return cursor.fetchall()

@connection.connection_handler
def count_by_user(cursor, userid):
    """ function to count activity"""
    query = f"""
            SELECT COUNT(user_answer.user_id={userid}) AS answers, COUNT(user_comment.user_id={userid}) AS comment,
            COUNT(user_question.user_id={userid} as question;    
    """


@connection.connection_handler
def gain_reputation(cursor, user_name, points: int):
    query=f"""
            UPDATE users
            SET user_rep = user_rep+{points}
            WHERE user_name = '{user_name}';
    """
    cursor.execute(query)


@connection.connection_handler
def lose_reputation(cursor, user_name, points):
    query=f"""
            UPDATE users
            SET user_rep = user_rep-{points}
            WHERE user_name = '{user_name}';
    """
    cursor.execute(query)


@connection.connection_handler
def add_user(cursor, user_name, user_password):
    """
    returns username when adding a new user
    """
    from datetime import datetime
    dt = datetime.now().strftime("%Y-%m-%d %H:%M")
    query = f"""
            INSERT INTO "users" (user_name, user_pass, date_reg, user_role, user_rep)
            VALUES ('{user_name}', '{user_password}', '{dt}', 'user', 0)
            RETURNING user_name, user_id"""
    cursor.execute(query, (user_name, user_password,))
    return cursor.fetchone()


@connection.connection_handler
def get_user_data_by_username(cursor, username):
    query = f"""
            SELECT * 
            FROM users
            WHERE user_name = '{username}'
            """
    cursor.execute(query, (username,))
    return cursor.fetchone()

@connection.connection_handler
def get_user_id_by_question_id(cursor, question_id):
    cursor.execute(f"""
            SELECT user_id as userid FROM users u
            JOIN question q ON u.user_id = g.id
            WHERE q.id = {question_id} 
    """)
    return cursor.fetchall()

@connection.connection_handler
def get_owner_question(cursor, question_id):
    """ return owner of question"""
    query = f"""
            SELECT user_name FROM users WHERE user_id=(
            SELECT user_id FROM user_question 
            WHERE user_question.question_id={question_id} );
            """
    cursor.execute(query)
    return cursor.fetchone()

@connection.connection_handler
def get_owner_comment(cursor, question_id):
    """ return owner of comment"""
    query = f"""
            SELECT user_name FROM users WHERE user_id=(
            SELECT user_id FROM user_comment 
            WHERE user_comment.comment_id={question_id} );           
            """
    cursor.execute(query)
    return cursor.fetchone()

@connection.connection_handler
def get_onwer_answer(cursor, answer_id):
    """return owner of answer"""
    query = f"""
            SELECT user_name FROM users u LEFT JOIN user_answer a ON u.user_id=a.user_id WHERE a.answer_id={answer_id};
            """
    cursor.execute(query)
    return cursor.fetchone()

@connection.connection_handler
def add_question_to_user(cursor, username):
    """ add new question to user account"""
    query = f"""
            INSERT INTO user_question (question_id, user_id)
            VALUES ((SELECT MAX(id) FROM question), (SELECT user_id FROM users WHERE user_name='{username}'));
            """
    cursor.execute(query)

@connection.connection_handler
def add_anser_to_user(cursor, username):
    """ add new answer to user account"""
    query = f"""
            INSERT INTO user_answer (answer_id, user_id)
            VALUES ((SELECT MAX(id) FROM answer), (SELECT user_id FROM users WHERE user_name='{username}'));    
            """
    cursor.execute(query)

@connection.connection_handler
def add_comment_to_user(cursor, username):
    """ add new comment to user account"""
    query = f"""
            INSERT INTO user_comment (comment_id, user_id)
            VALUES ((SELECT MAX(id) FROM comment), (SELECT user_id FROM users WHERE user_name='{username}'));    
            """
    cursor.execute(query)

