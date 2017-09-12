from .exceptions import (CannotCreateEmptyNote, InvalidExpirationFieldValue, 
                         ExpirationFieldEmpty)
from flask import Flask, request, jsonify, render_template, send_file
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from .helper_functions import create_file
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
    
    try:
        new_note.set_title(title)
        new_note.set_expiration(expiration)
        new_note.set_content(content)
    except InvalidExpirationFieldValue:
        # When expiration is not a number in 0..5
        return jsonify({'error': 'EXPIRATION_FIELD_INVALID'})
    except ExpirationFieldEmpty:
        return jsonify({'error': 'EXPIRATION_FIELD_EMPTY'})
    except CannotCreateEmptyNote:
        return jsonify({'error': 'CONTENT_FIELD_EMPTY'})
    else:
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
        return render_template('404.html')
    else:
        if note.is_expired():
            return render_template('404.html')
        else:
            if action == 'raw':
                return render_template('raw-display.html', title=note.title, 
                                       content=note.content)
            elif action == 'download':
                filename = note.hash
                content = note.content
                file_path = create_file(filename, content)
                return send_file(file_path, mimetype='txt', as_attachment=True)
            else:
                return render_template('display.html', title=note.title,
                                       content=note.content)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404