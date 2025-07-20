import os
import uuid
from datetime import datetime

def allowed_file(filename, allowed_extensions):
    """
    Check if uploaded file has allowed extension
    
    Args:
        filename (str): Name of the uploaded file
        allowed_extensions (set): Set of allowed file extensions
        
    Returns:
        bool: True if file extension is allowed, False otherwise
        
    Example:
        >>> allowed_file('image.jpg', {'jpg', 'png'})
        True
        >>> allowed_file('document.pdf', {'jpg', 'png'})
        False
    """
    return ('.' in filename and 
            filename.rsplit('.', 1)[1].lower() in allowed_extensions)

def get_unique_filename(original_filename, upload_folder):
    """
    Generate unique filename to prevent conflicts
    
    Args:
        original_filename (str): Original filename from upload
        upload_folder (str): Path to upload directory
        
    Returns:
        str: Unique filename that doesn't exist in upload folder
        
    Strategy:
        1. Try original filename first
        2. If exists, add timestamp and UUID
        3. Keep original extension
    """
    
    # Try original filename first
    if not os.path.exists(os.path.join(upload_folder, original_filename)):
        return original_filename
    
    # Generate unique filename
    name, ext = os.path.splitext(original_filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    
    unique_filename = f"{name}_{timestamp}_{unique_id}{ext}"
    
    return unique_filename

def format_file_size(size_bytes):
    """
    Convert file size in bytes to human-readable format
    
    Args:
        size_bytes (int): File size in bytes
        
    Returns:
        str: Formatted file size (e.g., "2.5 MB", "1.2 KB")
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def validate_image_dimensions(image_path, max_width=4000, max_height=4000):
    """
    Validate image dimensions to prevent memory issues
    
    Args:
        image_path (str): Path to image file
        max_width (int): Maximum allowed width
        max_height (int): Maximum allowed height
        
    Returns:
        tuple: (is_valid, width, height, error_message)
    """
    try:
        import cv2
        
        # Read image to get dimensions
        img = cv2.imread(image_path)
        if img is None:
            return False, 0, 0, "Could not read image file"
        
        height, width = img.shape[:2]
        
        if width > max_width or height > max_height:
            return False, width, height, f"Image too large: {width}x{height}. Max: {max_width}x{max_height}"
        
        return True, width, height, None
        
    except Exception as e:
        return False, 0, 0, f"Error validating image: {str(e)}"

def cleanup_old_files(directory, max_age_hours=24):
    """
    Clean up old uploaded files to save disk space
    
    Args:
        directory (str): Directory to clean
        max_age_hours (int): Maximum age of files in hours
        
    Returns:
        int: Number of files deleted
    """
    if not os.path.exists(directory):
        return 0
    
    deleted_count = 0
    current_time = datetime.now()
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        if os.path.isfile(filepath):
            # Get file modification time
            file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            age_hours = (current_time - file_time).total_seconds() / 3600
            
            if age_hours > max_age_hours:
                try:
                    os.remove(filepath)
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting file {filepath}: {e}")
    
    return deleted_count