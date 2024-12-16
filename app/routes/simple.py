from flask import Blueprint, render_template, redirect
from ..forms import NewInstrument
from ..models import db, Instrument

bp = Blueprint("simple", __name__)

@bp.route('/')
def home():
    return render_template("main_page.html")

@bp.route('/new-instrument')
def get_form():
    form = NewInstrument()
    return render_template("simple_form.html", form=form)

@bp.route('/new_instrument', methods=['GET', 'POST'])
def create_instrument():
    form = NewInstrument()
    if form.validate_on_submit():
        data = Instrument()
        form.populate_obj(data)
        db.session.add(data)
        db.session.commit()
        return redirect('/')
    return "Bad Data", 400

@bp.route('/instrument_data')
def instrument_data():
    instruments = Instrument.query.all()
    return render_template('instrument_data.html', instruments=instruments)
