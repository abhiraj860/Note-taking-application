from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from website import ml_model
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 
        switch_state = request.form.get('switchState')  # Retrieve the switch state
        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            if switch_state:
                # Check if there is a note for the current date in the database
                current_date = datetime.now().date()
                current_time = datetime.now().time()
                latest_note = Note.query.filter_by(user_id=current_user.id, currDate=current_date).order_by(Note.currtime.desc()).first()

            # Compute sentiment using the nltk_vader_sentiment function
            sentiment, sentimentColor = ml_model.nltk_vader_sentiment(note)
            new_note = Note(data=note, user_id=current_user.id, sentiment=sentiment, sentimentColor = sentimentColor)
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')    
        return redirect(url_for('views.home'))  # Redirect to the home page to avoid form resubmission    
    # Access the user's first name
    first_name = current_user.first_name
    
    # Retrieve the day and date from the database
    notes = Note.query.filter_by(user_id=current_user.id).all()
    note_data = [(note.currDate, note.day, note.month, note.sentimentColor) for note in notes]
    return render_template("home.html", user=current_user, first_name = first_name, note_data=note_data)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
