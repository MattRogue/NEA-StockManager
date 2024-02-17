from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import StaffType

views = Blueprint('views', __name__)


@views.route('/home/')
@login_required
def home():
    return render_template(
        'home.html',
        user=current_user
    )

@views.route('/inventory/')
@login_required
def inventory():
    return render_template(
        'inventory.html',
        user=current_user
    )
    
@views.route('orders')
@login_required
def orders():
    return render_template(
        'orders.html',
        user=current_user
    )

@views.route('settings')
@login_required
def settings():
    return render_template(
        'settings.html',
        user=current_user
    )