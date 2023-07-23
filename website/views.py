from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
from website import ml_model
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    if request.method == 'POST': 
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
    ###########################################################################################################
    searchDate = request.args.get('searchDate')
    if 'searchButton' in request.args:
        notesSearch = Note.query.filter_by(user_id=current_user.id).filter(Note.currDate == searchDate).all()
        if not notesSearch:
            flash('Data Not Found', category='error')
        else:
            note_data = [(note.currDate, note.day, note.month, note.sentimentColor, note.data, note.id) for note in notesSearch]
            flash('Search Complete for' + searchDate, category='success')
            return render_template("home.html", user=current_user, first_name = first_name, note_data=note_data, latest_switch_state = latest_switch_state)
    
    ##########################################################################################################
    
    note_data = [(note.currDate, note.day, note.month, note.sentimentColor) for note in notes]
    return render_template("home.html", user=current_user, first_name = first_name, note_data=note_data, latest_switch_state = latest_switch_state)


# @views.route('/search-results', methods=['GET', 'POST'])
# def search_results():
#     search_date = request.args.get('searchDate')

#     # Validate the search_date (you can add more complex validation logic as needed)
#     if not search_date:
#         return jsonify(error='No search date provided.')

#     # Process the search_date data as needed
#     # For example, you can check if it's a valid date or perform some other operations.
#     try:
#         # In this example, we create a simple search result HTML snippet.
#         search_result_html = f'Search results for: {search_date}'
#         return search_result_html
#     except Exception as e:
#         return jsonify(error=f'Error processing search: {str(e)}')




# @views.route('/delete-note', methods=['POST'])
# def delete_note():  
#     note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})
