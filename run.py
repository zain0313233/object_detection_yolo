import os
from app import create_app
from app.config import config

config_name = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config[config_name])
if __name__ == '__main__':
    print("🚀 Starting Object Detection Flask Application...")
    print(f"📝 Configuration: {config_name}")
    print(f"🐛 Debug Mode: {app.config.get('DEBUG')}")
    print(f"📁 Upload Folder: {app.config.get('UPLOAD_FOLDER')}")
    app.run(host='127.0.0.1', port=5000,debug=app.config.get('DEBUG', False),threaded=True)
