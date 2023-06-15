import data_handler
from werkzeug.utils import secure_filename
import os
from markupsafe import Markup


UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'webp'}


def vote_up_or_down(vote_number, vote_type):
    if vote_type == 'up':
        vote_number['vote_number'] += 1
    else:
        vote_number['vote_number'] -= 1
    return vote_number['vote_number']


def deciding_where_to_redirect(comments, comment_id, answer_id, question_id):
    for comment in comments:
        if comment["question_id"] == int(question_id) and comment["id"] == comment_id:
            return "question"

        elif comment["answer_id"] == int(answer_id) and comment["id"] == comment_id:
            return "answer"


def order_questions(order_by, order):
    if order is not None:
        questions = data_handler.list_questions(order_by, order)
    else:
        order_by = 'submission_time'
        order = 'DESC'
        questions = data_handler.list_questions(order_by, order)
    return questions

def upload_image(image):
    if '.' in image.filename and image.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        filename = secure_filename(image.filename)
        image.save(os.path.join(UPLOAD_FOLDER, filename))

def marking(dictionary, search_phrase):
    dictionary['message'] = dictionary['message'].casefold()
    dictionary['message'] = Markup(dictionary['message'].replace(search_phrase, f"<mark>{search_phrase}</mark>"))
    dictionary['title'] = dictionary['title'].casefold()
    dictionary['title'] = Markup(dictionary['title'].replace(search_phrase, f"<mark>{search_phrase}</mark>"))

def tag_validate(tag):
    """Tag validate to avoid tag as Nonetype object"""
    if tag !=None:
        return tag['name']
    else:
        tag=''
        return tag

def tag_count():
    """function to count questions by tags"""
    quests = {
        'python': 0,
        'sql': 0,
        'css': 0,
    }
    counter = data_handler.count_tags(1)
    quests['python'] = counter['count']
    counter = data_handler.count_tags(2)
    quests['sql'] = counter['count']
    counter = data_handler.count_tags(3)
    quests['css'] = counter['count']
    return quests
    
def gain_reputation_answer(rep):
    if rep == 'up':
        return 10
    if rep == 'down':
        return 2

def gain_reputation_question(rep):
    if rep == 'up':
        return 5
    if rep == 'down':
        return 2
