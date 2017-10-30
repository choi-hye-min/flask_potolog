import sys
from photolog import create_app

application = create_app()

if __name__ == '__main__':
    print("start server")
    application.run(host='0.0.0.0', port=5000, debug=True)