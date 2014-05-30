from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from idl import app
from idl.database import forum_session
from idl.database.models import ForumBoard, ForumMessage, ForumTopic
from idl.views.utils import get_latest_games, render_template

@app.route('/')
def home():
    board_id = app.config['NEWS_FORUM_BOARD_ID']
    try:
        board = forum_session.query(ForumBoard).get(board_id)
        q = forum_session.query(ForumTopic)
        q = q.filter(ForumTopic.id_board==board_id)
        topic_message_ids = [topic.id_first_msg for topic in q.all()]
        q = forum_session.query(ForumMessage)
        q = q.filter(ForumMessage.id_msg.in_(topic_message_ids))
        q = q.order_by(ForumMessage.poster_time.desc())
        posts = q.limit(10).all()
    except (MultipleResultsFound, NoResultFound):
        posts = []
    return render_template('home.mako', **{
        'section': 'home',
        'subsection': 'news',
        'posts': posts,
        'games': get_latest_games()
    })

