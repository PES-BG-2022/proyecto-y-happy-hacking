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

@views.route('/converxrango', methods=['GET', 'POST'])
@login_required
def conversor_rango():
    if request.method == 'POST':
        desde = request.form.get('fecha_inicio')
        hasta = request.form.get('fecha_fin')


        if not desde:
            flash("Ingrese fecha de inicio")
            # resultado = tipo_cambio.convertir_usd_a_gtq(float(usd))
            # new_note = Note(data=resultado, user_id=current_user.id)
            # db.session.add(new_note)
            # db.session.commit()
            # flash('¡Dólares convertidos a quetzales!', category='success')
        if not hasta:
            flash("Ingrese fecha de fin")
            print(hasta)
            # resultado = tipo_cambio.convertir_gtq_a_usd(float(gtq))
            # new_note = Note(data=resultado, user_id=current_user.id)
            # db.session.add(new_note)
            # db.session.commit()
            # flash('¡Quetzales convertidos a dólares!', category='success')
        if (desde and hasta):
            desde = desde[-2:] + "-" + desde[-5:-3] + "-" + desde[-10:-6]
            if (int(desde[3]) == 0):
                desde = desde[:3] + desde[4:]
            if (int(desde[0])==0):
                desde = desde[1:]
            hasta = hasta[-2:] + "-" + hasta[-5:-3] + "-" + hasta[-10:-6]
            if (int(hasta[3]) == 0):
                hasta = hasta[:3] + hasta[4:]
            if (int(hasta[0])==0):
                hasta = hasta[1:]
            tipo_cambio.obtener_tasas_por_rango(desde, hasta)

    return render_template("conversor_rango.html", user=current_user)

@views.route('/resultadorango', methods=['GET', 'POST'])
@login_required
def resultado_rango():
    return render_template("resultado_rango.html", user=current_user)

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
