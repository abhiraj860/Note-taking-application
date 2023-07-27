from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
from website import ml_model
from datetime import datetime
from flask import jsonify

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST' and 'uploadButton' in request.form: 
        note = request.form.get('note')#Gets the note from the HTML 
        switch_state = request.form.get('switchState')  # Retrieve the switch state
        switch_state_bool = bool(switch_state)
        
        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            if switch_state:
                # Check if there is a note for the current date in the database
                current_date = datetime.now().date()
                current_time = datetime.now().time()
            
                latest_note = Note.query.filter_by(user_id=current_user.id, currDate=current_date).order_by(Note.id.desc()).first()
                if latest_note:
                    latest_note.data = latest_note.data + '\n' + note
                    latest_note.sentiment, latest_note.sentimentColor = ml_model.nltk_vader_sentiment(latest_note.data)
                    latest_note.currtime = current_time  # Update the current time of the note
                    latest_note.day = current_date.strftime("%A")  # Set the current day for the new note
                    latest_note.month = current_date.strftime('%B')
                    latest_note.switch_state = switch_state_bool
                    try:
                        db.session.commit()
                        flash('Note appended!', category='success')
                    except Exception as e:
                        flash(f'Error: {str(e)}', category='error')
                    return redirect(url_for('views.home')) 
                else:
                    # Compute sentiment using the nltk_vader_sentiment function
                    sentiment, sentimentColor = ml_model.nltk_vader_sentiment(note)
                    new_note = Note(data=note, user_id=current_user.id, sentiment=sentiment, sentimentColor = sentimentColor, switch_state = switch_state_bool)
                    db.session.add(new_note) #adding the note to the database 
                    db.session.commit()
                    flash('Note added!', category='success')    
                    return redirect(url_for('views.home'))  # Redirect to the home page to avoid form resubmission     
            # Compute sentiment using the nltk_vader_sentiment function
            sentiment, sentimentColor = ml_model.nltk_vader_sentiment(note)
            # switch_state_bool = bool(switch_state)
            new_note = Note(data=note, user_id=current_user.id, sentiment=sentiment, sentimentColor = sentimentColor, switch_state = switch_state_bool)
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')    
        return redirect(url_for('views.home'))  # Redirect to the home page to avoid form resubmission    
    # Access the user's first name
    first_name = current_user.first_name
    
    # Retrieve the day and date from the database
    notes = Note.query.filter_by(user_id=current_user.id).all()
    get_switch_state = Note.query.filter_by(user_id=current_user.id).order_by(Note.id.desc()).first()
    latest_switch_state = "checked" if get_switch_state.switch_state else "" 
    note_data = [(note.currDate, note.day, note.month, note.sentimentColor, note.data, note.id) for note in notes]
    return render_template("home.html", user=current_user, first_name = first_name, note_data=note_data, latest_switch_state = latest_switch_state)

@views.route('/searchList', methods=['POST'])
@login_required
def searchList():
    if request.method == 'POST': 
        searchDate = request.form.get('searchDate')
        notesSearch = Note.query.filter_by(user_id=current_user.id).filter(Note.currDate == searchDate).all()
        if not notesSearch:
            return render_template("dataNotFound.html", searchDate = searchDate)
        else:
            note_data = [(note.currDate, note.day, note.month, note.sentimentColor, note.data, note.id) for note in notesSearch]
            return render_template("searchList.html", note_data=note_data)
    return redirect(url_for('views.home'))

@views.route('/searchAll', methods=['POST'])
@login_required
def searchAll():
    if request.method == 'POST': 
        notes = Note.query.filter_by(user_id=current_user.id).all()
        note_data = [(note.currDate, note.day, note.month, note.sentimentColor, note.data, note.id) for note in notes]
        return render_template("searchList.html", note_data=note_data)
    return redirect(url_for('views.home'))


@views.route('/toggleSwitch', methods=['POST'])
@login_required
def handle_switch_state():
    # Get the switch state data from the request JSON
    switch_state = request.json.get('switchState')

    # Here you can process the switch state as needed
    # For this example, we'll simply print the state
    switch_state_bool = bool(switch_state)
    print('Switch state received:', switch_state_bool)
    latest_note = Note.query.filter_by(user_id=current_user.id).order_by(Note.id.desc()).first()
    latest_note.switch_state = switch_state_bool
    db.session.commit()

    # You can also send a response back to the frontend if required
    return jsonify({'message': 'Switch state received successfully.'})

    