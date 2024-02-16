from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import StaffType

views = Blueprint('views', __name__)


@views.route('/home/')
@login_required
def home():
    return render_template('home.html',
        user=current_user,
        StaffType=StaffType
    )



