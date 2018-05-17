from flask import current_app as app, render_template, request, redirect, jsonify, url_for, Blueprint
from CTFd.utils import admins_only, is_admin, cache, update_check
from CTFd.models import db, Teams, Solves, Awards, Challenges, WrongKeys, Keys, Tags, Files, Tracking, Pages, Config, DatabaseError, CheatPenalty

from CTFd import utils

admin_supervise = Blueprint('admin_supervise', __name__)


@admin_statistics.route('/admin/supervise')
@admins_only
def admin_supervise():
    return render_template('admin/supervise.html')
