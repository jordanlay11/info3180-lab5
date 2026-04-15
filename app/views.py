from app import app
from flask import render_template, request, jsonify, send_file
import os
from . import db
from app.models import Movies
from app.forms import MovieForm
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route("/api/v1/movies", methods=['POST', 'GET'])
def movies():
    if request.method == 'POST':
        form = MovieForm()  
        
        if form.validate_on_submit():
            title = form.title.data
            description = form.description.data
            poster = form.poster.data

            filename = secure_filename(form.poster.data.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            poster.save(file_path)
            poster = file_path

            new_movie = Movies(title=title, description=description, poster=poster)
            db.session.add(new_movie)
            db.session.commit()

            return jsonify(message="Movie successfully added", title=title, description=description, poster=poster), 201
        else:
            return jsonify(form_errors=form_errors(form)), 400
    
    if request.method == 'GET':
        movies = Movies.query.all()
        movies_list = []
        for movie in movies:
            movies_list.append({
                'id': movie.id,
                'title': movie.title,
                'description': movie.description,
                'poster': movie.poster
            })
        return jsonify(movies=movies_list)
        
@app.route('/api/v1/csrf-token', methods=['GET']) 
def get_csrf(): 
    return jsonify({'csrf_token': generate_csrf()})      

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404