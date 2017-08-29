from .exceptions import CannotCreateEmptyNote, InvalidExpirationFieldValue
from flask import Flask, request, jsonify, render_template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import Base, Notes


engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DatabaseSession = sessionmaker(bind=engine)
session = DatabaseSession()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_page():
    return render_template('form.html')


@app.route('/notes', methods=['POST'])
def add_note():
    title = request.form.get('title')
    expiration = request.form.get('expiration')
    content = request.form.get('content')
    
    new_note = Notes()

    new_note.set_title(title)
    try:
        new_note.set_expiration(expiration)
    except InvalidExpirationFieldValue:
        # When expiration is not a number in 0..5
        return jsonify({'error': 'EXPIRATION_FIELD_INVALID'})

    try:
        new_note.set_content(content)
    except CannotCreateEmptyNote:
        return jsonify({'error': 'CONTENT_FIELD_INVALID'})

    new_note.set_hash()
    session.add(new_note)
    session.commit()
    return jsonify(note=new_note.serialize)


@app.route('/notes/<string:hash>', methods=['GET'])
def get_note(hash):
    action = request.args.get('action')
    try:
        note = session.query(Notes).filter_by(hash=hash).one()
    except NoResultFound:
        return render_template('404.html', hash=hash)
    else:
        if note.is_expired():
            return render_template('404.html', hash=hash)
        else:
            if action == 'raw':
                return render_template('raw-display.html', title=note.title, 
                                       content=note.content)
            else:
                return render_template('display.html', title=note.title,
                                       content=note.content)
