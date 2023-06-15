import data_handler
import bonus_questions as bq
import util
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_bootstrap import Bootstrap
from password_handler import get_hashed_password, verify_password


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = '$^fg4hy5hGF'

@app.route('/')
def get_last_5_questions_by_time():
    if "username" in session:
        questions = data_handler.get_last_five_question_by_time()
        return render_template("list_questions.html",
                           data=questions,
                           user=session.get('username'),
                           title="Main page")
    else:
        user = None
    questions = data_handler.get_last_five_question_by_time()
    return render_template("list_questions.html",
                           data=questions,
                           user=user,
                           title="Main page")

@app.route('/about')
def about():
    """render the section about"""
    
    return render_template('about.html', user=session.get('username'))

@app.route('/list')
def list_question():
    order_by_options = {'submission_time': 'Submission time', 'view_number': 'View number', 'vote_number': 'Vote number', 'title': 'Title'}
    order_options = ['DESC', 'ASC']
    order_by = request.args.get('order_by')
    order = request.args.get('order')
    questions = util.order_questions(order_by, order) 
    return render_template("list_questions.html",
                           data=questions,
                           title="List questions",
                           select_options=order_by_options,
                           order_options=order_options,
                           order_by=order_by,
                           user=session.get('username'),
                           order=order)

@app.route("/")
def main():
    """render the main page"""
    data = data_handler.get_questions()
    return render_template("list_questions.html", data=data, user=session.get('username'))

@app.route('/search')
def search():
    """ function to search in database"""
    search = request.args.get('search')
    search_by_tags = request.args.get('search-by-tags')
    if search_by_tags != None:
        if search_by_tags == 'python':
            question_data = data_handler.search_by_tags(1)
            return render_template("list_questions.html", data=question_data, user=session.get('username'))
        elif search_by_tags == 'sql':
            question_data = data_handler.search_by_tags(2)
            return render_template("list_questions.html", data=question_data, user=session.get('username'))
        elif search_by_tags == 'css':
            question_data = data_handler.search_by_tags(3)
            return render_template("list_questions.html", data=question_data, user=session.get('username'))
    question_data = data_handler.search_question(search)
    return render_template("list_questions.html", data=question_data, user=session.get('username'))
    #return render_template("list_questions.html", data=data)

@app.route('/question/<int:question_id>')
def display_question(question_id):
    tag = data_handler.show_tag(question_id)
    question = data_handler.display_question(question_id)
    answers = data_handler.get_answers_for_question(question_id)
    print(answers)
    comments = data_handler.get_comments_for_question(question_id)
    data_handler.increase_view_number(question_id)
    #user_id = session['userid'] if ('username' in session) else -1
    #question_user_id = data_handler.get_user_id_by_question_id(question_id)
    owner = data_handler.get_owner_question(question_id)
    ownerc = data_handler.get_owner_comment(question_id) #!
    ownera = data_handler.get_onwer_answer(question_id)  #!
    return render_template("display_question.html",
                           question_id=question_id,
                           question=question,
                           answers=answers,
                           comments=comments,
                           tag=util.tag_validate(tag),
                           owner=owner,
                           ownerc=ownerc,
                           ownera=ownera,
                           user=session.get('username'),
                           title="Display question")


@app.route('/add-question', methods=["GET"])
def route_question():
    user = session.get('username')
    return render_template("add_question.html",
                            user=user,
                           title="Add question")


@app.route('/add_question', methods=["POST"])
def add_question():
    """ add new question to database"""
    #if "username" not in session:
    user = session.get('username')
    if user == None:
        flash('Only registered users!')
        return redirect(url_for("login"))
    else:
        util.upload_image(request.files['image'])
        image = request.files["image"]
        new_question = {#"user_id": session['userid'],
                        "view_number": 0,
                        "vote_number": 0,
                        "title": request.form.get("title"),
                        "message": request.form.get("message"),
                        "image": request.files['image'].filename}
        tag_name = request.form.get("tag")
        data_handler.add_new_data_to_table(new_question, 'question') 
        if tag_name == 'python':
            data_handler.add_new_tag(1)
        elif tag_name == 'sql':
            data_handler.add_new_tag(2)
        elif tag_name == 'css':
            data_handler.add_new_tag(3)
        data_handler.add_question_to_user(session['username'])
        return redirect(url_for("list_question"))

@app.route('/question/<question_id>/are-you-sure', methods=["GET"])
def confirm_delete_question(question_id):

    return render_template("confirm_delete_question.html",
                           question_id=question_id,
                           title="Are you sure you want to delete this question?")


@app.route('/question/<question_id>/are-you-sure', methods=["POST"])
def delete_question(question_id):
    data_handler.delete_question(question_id)
    data_handler.delete_tag(question_id)

    return redirect(url_for("list_question"), user=session.get('username'))


@app.route('/question/<question_id>/new-answer', methods=["GET"])
def route_new_answer(question_id):
    user = session.get('username')
    return render_template("new_answer.html",
                           question_id=question_id,
                           user=user,
                           title="New answer")


@app.route('/question/<question_id>/new-answer', methods=["POST"])
def post_answer(question_id):
    if "username" not in session:
        return redirect(url_for("login"))

    util.upload_image(request.files['image'])
    #image = request.files["image"]
    new_answer = {'vote_number': 0,
                  'question_id': question_id,
                  'message': request.form.get('message'),
                  'image': request.files['image'].filename,
                  'user_id': session['userid']}
    data_handler.add_new_data_to_table(new_answer, 'answer')
    user=session.get('username')
    data_handler.add_anser_to_user(user)
    return redirect(url_for("display_question", question_id=question_id))


@app.route('/question/<int:question_id>/edit', methods=["GET"])
def route_edit_question(question_id):

    question_to_edit = data_handler.route_edit_question(question_id)

    return render_template("edit_question.html",
                           title="Edit question",
                           question=question_to_edit,
                           question_id=question_id,
                           user=session.get('username'))


@app.route('/question/<question_id>/edit', methods=["POST"])
def edit_question(question_id):
    if "username" not in session:
        return redirect(url_for("login"))

    question_id = request.args.get('question-id')

    edited_title = request.form['title']
    edited_message = request.form['message']
    data_handler.edit_question(question_id, edited_title, edited_message)

    return redirect(url_for("display_question",
                            question_id=question_id), user=session.get('username'))


@app.route('/question/<int:question_id>/vote')
def vote_for_question(question_id):
    user=session.get('username')
    rep_user= data_handler.get_onwer_answer(question_id)
    vote_type = request.args.get('vote_type')
    title = request.args.get('title')
    vote_number = data_handler.get_question_vote_number(question_id)
    increases_or_decreases_vote_number = util.vote_up_or_down(vote_number, vote_type)
    reputation = util.gain_reputation_question(vote_type)
    if vote_type == 'up':
        data_handler.gain_reputation(rep_user['user_name'], reputation)
    else:
        data_handler.lose_reputation(rep_user['user_name'], reputation)
    data_handler.update_question_vote_number(question_id, increases_or_decreases_vote_number)
    if title == 'Main page':
        return redirect(url_for("get_last_5_questions_by_time"))
    return redirect(url_for("list_question"))


@app.route('/answer/<answer_id>/vote')
def vote_for_answer(answer_id):
    question_id = request.args.get('question_id')
    vote_type = request.args.get('vote_type')
    vote_number = data_handler.get_answer_vote_number(question_id, answer_id)
    increases_or_decreases_vote_number = util.vote_up_or_down(vote_number, vote_type)
    reputation = util.gain_reputation_answer(vote_type)
    rep_user= data_handler.get_onwer_answer(answer_id)
    if vote_type == 'up':
        data_handler.gain_reputation(rep_user['user_name'], reputation)
    else:
        data_handler.lose_reputation(rep_user['user_name'], reputation)
    data_handler.update_answer_vote_number(question_id, answer_id, increases_or_decreases_vote_number)

    return redirect(url_for("display_question",
                            question_id=question_id))


@app.route('/answer/<answer_id>/edit', methods=["GET"])
def route_edit_answer(answer_id):

    question_id = request.args.get('question_id')
    answers = data_handler.get_answer_for_question_by_id(answer_id, question_id)

    return render_template('edit_answer.html',
                           answers=answers,
                           answer_id=answer_id,
                           question_id=question_id,
                           user=session.get('username'),
                           title="Edit answer")


@app.route('/answer/<answer_id>/edit', methods=["POST"])
def edit_answer(answer_id):
    if "username" not in session:
        return redirect(url_for("login"))

    question_id = request.args.get('question-id')
    new_answer = {'id': answer_id,
                'question_id': question_id,
                'message': request.form.get('message'),
                'image': None}
    data_handler.update_question_answer(new_answer)

    return redirect(url_for("display_question",
                            question_id=question_id))


@app.route('/answer/<int:answer_id>/are-you-sure', methods=["GET"])
def confirm_delete_answer(answer_id):
    question_id = request.args.get("question_id")

    return render_template("confirm_delete_answer.html",
                           answer_id=answer_id,
                           question_id=question_id,
                           title="Are you sure you want to delete this answer?")


@app.route('/answer/<int:answer_id>/delete', methods=["GET", "POST"])
def delete_answer(answer_id):
    if "username" not in session:
        flash('You are not logged in!')
        return redirect(url_for("login"))
    question_id = request.args.get("question_id")
    data_handler.delete_answer(answer_id)

    return redirect(url_for("display_question",
                            question_id=question_id))


@app.route('/question/<question_id>/new-comment', methods=["GET"])
def route_new_question_comment(question_id):
    user = session.get('username')
    return render_template('add_comment_for_question.html',
                           question_id=question_id,
                           user=user,
                           title='New comment')


@app.route('/question/<question_id>/new-comment', methods=["POST"])
def add_new_question_comment(question_id):
    if "username" not in session:
        flash('You are not logged in!')
        return redirect(url_for("login"))
    new_comment = {'question_id': question_id,
                    'answer_id': None,
                    'message': request.form.get("message"),
                    'edited_count': 0,
                   'user_id': session['userid']}
    data_handler.add_new_data_to_table(new_comment, 'comment')
    data_handler.add_comment_to_user(session['username'])

    return redirect(url_for("display_question",
                            question_id=question_id))


@app.route('/answer/<answer_id>/new-comment', methods=["GET"])
def route_new_answer_comment(answer_id):
    user = session.get('username')
    question_id = request.args.get("question_id")
    return render_template('add_comment_for_answer.html',
                           answer_id=answer_id,
                           question_id=question_id,
                           user=user,
                           title='New comment')


@app.route('/answer/<int:answer_id>/new-comment', methods=["POST"])
def add_new_answer_comment(answer_id):
    if "username" not in session:
        flash('You are not logged in!')
        return redirect(url_for("login"))
    question_id = request.args.get("question_id")
    new_comment = {
                    'question_id': None,
                    'answer_id': answer_id,
                    'message': request.form.get("message"),
                    'edited_count': 0,
                    'user_id': session['userid']
                    }
    data_handler.add_new_data_to_table(new_comment, 'comment')

    return redirect(url_for("show_answer_and_comments",
                            answer_id=answer_id,
                            question_id=question_id))


@app.route('/question/show-answer/<int:answer_id>', methods=["GET"])
def show_answer_and_comments(answer_id):
    question_id = request.args.get("question_id")
    answer = data_handler.get_answer_by_answer_id(answer_id)
    comments_for_answer = data_handler.get_comments_for_answer(answer_id)

    return render_template('display_answer_with_comments.html',
                           comments=comments_for_answer,
                           answer=answer,
                           answer_id=answer_id,
                           question_id=question_id,
                           title="Answer and comments")


@app.route('/comments/<int:comment_id>/are-you-sure', methods=["GET"])
def confirm_delete_comment(comment_id):
    question_id = request.args.get("question_id")
    answer_id = request.args.get("answer_id")

    return render_template("confirm_delete_comment.html",
                           comment_id=comment_id,
                           question_id=question_id,
                           answer_id=answer_id,
                           title="Are you sure you want to delete this comment?")


@app.route('/comments/<int:comment_id>/delete', methods=["GET", "POST"])
def delete_comment(comment_id):
    if "username" not in session:
        flash('You are not logged in!')
        return redirect(url_for("login"))
    question_id = request.args.get("question_id")
    answer_id = request.args.get("answer_id")
    comments = data_handler.get_all_comments()
    data_handler.delete_comment(comment_id)

    if answer_id is None:
        answer_id = 0

    decision = util.deciding_where_to_redirect(comments, comment_id, answer_id, question_id)

    if decision == "question":
        return redirect(url_for("display_question",
                                question_id=question_id))
    elif decision == "answer":
        return redirect(url_for("show_answer_and_comments",
                                answer_id=answer_id,
                                question_id=question_id))


@app.route('/comments/<comment_id>/edit', methods=["GET"])
def route_edit_comment(comment_id):
    question_id = request.args.get("question_id")
    comment_to_edit = data_handler.route_edit_comment(comment_id)

    return render_template("edit_comment.html",
                           comment_id=comment_id,
                           comment=comment_to_edit,
                           question_id=question_id,
                           title="Edit comment")


@app.route('/comments/<comment_id>/edit', methods=["POST"])
def edit_comment(comment_id):
    if "username" not in session:
        flash('You are not logged in!')
        return redirect(url_for("login"))
    question_id = request.args.get("question_id")
    updated_comment = request.form.get("message")

    data_handler.edit_comment(comment_id, updated_comment)

    return redirect(url_for("display_question",
                            question_id=question_id))

#NEW

@app.route("/user/<user_id>")
def user(user_id):
    user=session.get('username')
    userInfo = data_handler.get_user(user_id)
    userQuestions = data_handler.get_user_questions(user_id)
    userAnswers = data_handler.get_user_answers(user_id)
    userComments = data_handler.get_user_comments(user_id)
    #userdata = {'userinfo': data_handler.get_user(user_id),
    #            'questions': data_handler.get_user_questions(user_id),
    #            'answers': data_handler.get_user_answers(user_id),
    #            'comments': data_handler.get_user_comments(user_id)}
    return render_template("user.html", user=user,
                                        userInfo=userInfo,
                                        userQuestions=userQuestions,
                                        userAnswers=userAnswers,
                                        userComments=userComments)


@app.route("/users")
def users():
    users_data = data_handler.users_data()
    user=session.get('username')
    return render_template("users.html", users=users_data, log=user)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if 'username' in session:
        return redirect(url_for('list_question'))

    error_message = None
    if request.method == 'POST':

        new_username = request.form["email"]
        is_user_name_unique = False if data_handler.get_user_data_by_username(new_username) else True

        if not is_user_name_unique:
            error_message = "invalid registration process!"
        else:
            new_plain_user_password = request.form["password"]
            new_hashed_password = get_hashed_password(new_plain_user_password)
            user_data = data_handler.add_user(new_username, new_hashed_password)
            session['username'] = user_data["user_name"]
            session["userid"] = user_data["user_id"]
            return redirect(url_for('list_question'))
    return render_template("user-registration.html", error=error_message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect(url_for("list_question"))
    error_message = None
    if request.method == 'POST':
        username = request.form["email"]
        user_password = request.form["password"]
        stored_user_data = data_handler.get_user_data_by_username(username)
        stored_user_password = stored_user_data["user_pass"] if stored_user_data else None
        stored_user_id = stored_user_data["user_id"] if stored_user_data else None
        if stored_user_data and verify_password(user_password, stored_user_password):
            session["username"] = username
            session["userid"] = stored_user_id
            return redirect(url_for('list_question'))
        error_message = "failed login attempt!"
    return render_template("user-login.html", error=error_message)


@app.route('/answer/<answer_id>/mark', methods=['POST'])
def mark_answered(answer_id):
    question_id = request.args.get('question-id')
    data_handler.mark_answered(answer_id, question_id)
    file_data = data_handler.get_answer(answer_id)[0]
    user_id = file_data.get('user_id', '')
    data_handler.gain_reputation(user_id, 15)
    return redirect("/question/"+str(question_id))


@app.route('/answer/<answer_id>/unmark', methods=['POST'])
def unmark_answered(answer_id):
    question_id = request.args.get('question-id')
    data_handler.unmark_answered(answer_id, question_id)
    file_data = data_handler.get_answer(answer_id)[0]
    user_id = file_data.get('user_id', '')
    data_handler.lose_reputation(user_id, 15)
    return redirect("/question/"+str(question_id))


@app.route('/logout')
def logout():
    if "username" in session:
        session.pop("userid")
        session.pop("username")
        flash('You have been logout!')
    return redirect(url_for("list_question"))


@app.route('/stats')
def statistics():
    user=session.get('username')
    tags = util.tag_count()
    users = data_handler.count_users()
    return render_template('stats.html', tags=tags, users=users, user=user)

@app.route('/users')
def all_users():
    user=session.get('username')
    users = data_handler.users_data()
    return render_template('users.html', users=users, log=user)

@app.route("/bonus-questions")
def bonus():
    return render_template('bonus_questions.html', questions=bq.SAMPLE_QUESTIONS)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )