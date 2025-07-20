import os
from dotenv import load_dotenv
basedirectory = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedirectory,'..','.env'))
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    UPLOAD_FOLDER = os.path.join(basedirectory, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
    
  
    YOLO_CONFIG_PATH = os.path.join(basedirectory, '..', 'yolo_files', 'yolov4.cfg')
    YOLO_WEIGHTS_PATH = os.path.join(basedirectory, '..', 'yolo_files', 'yolov4.weights')
    YOLO_NAMES_PATH = os.path.join(basedirectory, '..', 'yolo_files', 'coco.names')
    
 
    CONFIDENCE_THRESHOLD = float(os.environ.get('CONFIDENCE_THRESHOLD') or 0.5)
    NMS_THRESHOLD = float(os.environ.get('NMS_THRESHOLD') or 0.4)
    
  
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENV = 'development'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENV = 'production'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
