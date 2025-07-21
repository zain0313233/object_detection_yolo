from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
import os
from werkzeug.utils import secure_filename
from app.utils.helpers import allowed_file, get_unique_filename
from app.utils.detection import detect_objects

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    Home page route
    
    This is our landing page where users can choose what they want to do:
    - Upload an image for detection
    - Use webcam for real-time detection
    - View previous results
    """
    return render_template('index.html')

@main_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    File upload route
    
    GET: Show upload form
    POST: Process uploaded file and redirect to results
    """
    
    if request.method == 'GET':
        return render_template('upload.html')
    
    if 'file' not in request.files:
        flash('No file selected!', 'error')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected!', 'error')
        return redirect(request.url)
    
    if file and allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
        try:
            filename = secure_filename(file.filename)
            filename = get_unique_filename(filename, current_app.config['UPLOAD_FOLDER'])
            
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('main.results', filename=filename))
            
        except Exception as e:
            flash(f'Error uploading file: {str(e)}', 'error')
            return redirect(request.url)
    else:
        flash('Invalid file type! Please upload an image file.', 'error')
        return redirect(request.url)

@main_bp.route('/results/<filename>')
def results(filename):
    """
    Results display route with object detection
    Shows object detection results for uploaded images
    """
    if not filename:
        flash('No image specified!', 'error')
        return redirect(url_for('main.upload'))
    
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        flash('Image not found!', 'error')
        return redirect(url_for('main.upload'))
    
    try:
        # Run object detection
        result_filename = detect_objects(filepath)
        
        return render_template('results.html',
                             original_filename=filename,
                             result_filename=result_filename,
                             original_url=url_for('static', filename=f'uploads/{filename}'),
                             result_url=url_for('static', filename=f'uploads/{result_filename}'))
    except Exception as e:
        current_app.logger.error(f"Detection failed: {str(e)}")
        flash(f'Object detection failed: {str(e)}', 'error')
        return redirect(url_for('main.upload'))

@main_bp.route('/webcam')
def webcam():
    """
    Real-time webcam detection route
    
    This will show a page with webcam feed and real-time object detection
    """
    return render_template('webcam.html')

@main_bp.route('/about')
def about():
    """
    About page route
    
    Information about the project and technology used
    """
    return render_template('about.html')

@main_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@main_bp.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500