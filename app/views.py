"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app,db
from flask import render_template, request, jsonify, send_file, send_from_directory
import os
from app.models import Movies
from app.forms import MovieForm
from flask_wtf.csrf import generate_csrf

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###
@app.route('/api/v1/movies',methods=['POST'])
def movies():
    mform = MovieForm()
    
    if mform.validate_on_submit():
        title = mform.title.data
        description = mform.description.data
        poster = mform.poster.data
        
        movie = Movies(title=title, description=description, poster=poster.filename)
        db.session.add(movie)
        db.session.commit()
        
        poster.save(os.path.join(app.config['UPLOAD_FOLDER'],poster.filename))
        response = {
        "message":"Movie Successfully added",
        "title":title,
        "poster":poster.filename,
        "description":description
        }
        return jsonify(response),201
    else:
        errors = form_errors(mform)
        eresponse = {"errors":errors}
        return jsonify(eresponse),400

# Here we define a function to collect form errors from Flask-WTF
# which we can later use

@app.route('/api/v1/movies',methods=['GET'])
def showmovies():
    movies = Movies.query.all()
    mlst = []
    for m in movies:
        mdata = {
            'id': m.id,
            'title':m.title,
            'description':m.description,
            'poster':f'/api/v1/posters/{m.poster}'
        }
        mlst.append(mdata)
    return jsonify({'movies':mlst})

@app.route('/api/v1/posters/<filename>',methods=['GET'])
def getposter(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

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

@app.route('/api/v1/csrf-token',methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token':generate_csrf()})

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
