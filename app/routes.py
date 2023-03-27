from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import PhoneForm, LoginForm, AddressForm, SearchForm
from app.models import Phone, Address
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/', methods=["GET", "POST"])
def index():
    addresses = Address.query.all()
    form = SearchForm()
    if form.validate_on_submit():
        search_term = form.search_term.data
        # posts = Post.query.filter(Post.title.ilike(f"%{search_term}%")).all()
        addresses = db.session.execute(
            db.select(Address).where(
                (Address.street_name.ilike(f"%{search_term}%")) | 
                (Address.city.ilike(f"%{search_term}%")) | 
                (Address.state.ilike(f"%{search_term}%")) )).scalars().all()

    return render_template('index.html', addresses=addresses, form=form)

@app.route('/add-phone', methods=["GET", "POST"])
def add_phone():
    print("add a phone user...")
    form = PhoneForm()
    # Check if the form was submitted and is valid
    if form.validate_on_submit():
        first = form.first_name.data
        last = form.last_name.data
        phone = form.phone_number.data
        password = form.password.data
        print(first, last, phone, password)
        check_phone = db.session.execute(db.select(Phone).filter(Phone.phone_number == phone)).scalars().all()
        if check_phone:
            # Flash a message saying that user with email/username already exists
            flash("That phone number already exists", "warning")
            return redirect(url_for('add_phone'))

        new_phone = Phone(first_name=first, last_name=last, phone_number=phone, password=password)
        flash(f"{new_phone.first_name} {new_phone.last_name} {new_phone.phone_number} has been added to the phone book", "success")
        return redirect(url_for('index'))
    return render_template('add_phone.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Form Validated:')
        phone = form.phone_number.data
        password = form.password.data
        print(phone, password)
        # Check if there is a user with username and that password
        user = Phone.query.filter_by(phone_number=phone).first()
        if user is not None and user.check_password(password):
            # If the user exists and has the correct password, log them in
            login_user(user)
            flash(f'You have successfully logged in as {phone}', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username and/or password. Please try again', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have logged out", "info")
    return redirect(url_for('index'))


@app.route('/create', methods=["GET", "POST"])
@login_required
def create_address():
    form = AddressForm()
    if form.validate_on_submit():
        # Get the data from the form
        street_name = form.street_name.data
        number = form.number.data
        unit = form.unit.data or None
        postal_code = form.postal_code.data
        city = form.city.data
        state = form.state.data

        # Create an instance of Address with form data AND auth user ID
        new_address = Address(street_name=street_name, number=number, unit=unit, 
            postal_code=postal_code, city=city, state=state, phone_id=current_user.id)
        flash(f"{new_address} has been created!", "success")
        return redirect(url_for('index'))
    return render_template('create_address.html', form=form)


@app.route('/edit/<address_id>', methods=["GET", "POST"])
@login_required
def edit_address(address_id):
    form = AddressForm()
    address_to_edit = Address.query.get_or_404(address_id)
    # Make sure that the address author is the current user
    if address_to_edit.phone != current_user:
        flash("You do not have permission to edit this address", "danger")
        return redirect(url_for('index'))

    # If form submitted, update Address
    if form.validate_on_submit():
        # update the address with the form data
        address_to_edit.street_name = form.street_name.data
        address_to_edit.number = form.number.data
        address_to_edit.unit = form.unit.data or None
        address_to_edit.postal_code = form.postal_code.data
        address_to_edit.city = form.city.data
        address_to_edit.state = form.state.data

        # Commit that to the database
        db.session.commit()
        flash(f"{address_to_edit} has been edited!", "success")
        return redirect(url_for('index'))

    # Pre-populate the form with Address To Edit's values
    form.street_name.data = address_to_edit.street_name
    form.number.data = address_to_edit.number
    form.unit.data = address_to_edit.unit
    form.postal_code.data = address_to_edit.postal_code
    form.city.data = address_to_edit.city
    form.state.data = address_to_edit.state
    
    return render_template('edit_address.html', form=form, address=address_to_edit)


@app.route('/delete/<address_id>')
@login_required
def delete_address(address_id):
    address_to_delete = Address.query.get_or_404(address_id)
    if address_to_delete.phone != current_user:
        flash("You do not have permission to delete this address", "danger")
        return redirect(url_for('index'))

    db.session.delete(address_to_delete)
    db.session.commit()
    flash(f"{address_to_delete} has been deleted", "info")
    return redirect(url_for('index'))