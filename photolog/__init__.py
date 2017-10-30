import os
from flask import Flask, render_template, request, url_for

def print_settings(config):
    print('========================================================')
    print('SETTINGS for PHOTOLOG APPLICATION')
    print('========================================================')
    for key, value in config:
        print('%s=%s' % (key, value))
    print('========================================================')

def not_found(error):
    return render_template('404.html'), 404

def server_error(error):
    err_msg = str(error)
    return render_template('500.html', err_msg=err_msg), 500

def url_foer_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

def create_app(config_filepath='resource/config.cfg'):
    photolog_app = Flask(__name__)

    # 환경변수 가져옴
    from photolog.photolog_config import PhotologConfig
    photolog_app.config.from_object(PhotologConfig)
    photolog_app.config.from_pyfile(config_filepath, silent=True)
    print_settings(photolog_app.config.items())

    # 로그 초기화
    from photolog.photolog_logger import Log
    log_filepath = os.path.join(photolog_app.root_path, photolog_app.config['LOG_FILE_PATH'])
    Log.init(log_filepath=log_filepath)