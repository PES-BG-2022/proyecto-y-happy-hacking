from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from . import tipo_cambio

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        usd = request.form.get('usd')
        gtq = request.form.get('gtq')


        if (usd):
            resultado = tipo_cambio.convertir_usd_a_gtq(float(usd))
            new_note = Note(data=resultado, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('¡Dólares convertidos a quetzales!', category='success')
        elif (gtq):
            resultado = tipo_cambio.convertir_gtq_a_usd(float(gtq))
            new_note = Note(data=resultado, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('¡Quetzales convertidos a dólares!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
