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
    # print_settings(photolog_app.config.items())

    # 로그 초기화
    from photolog.photolog_logger import Log
    log_filepath = os.path.join(photolog_app.root_path, photolog_app.config['LOG_FILE_PATH'])
    Log.init(log_filepath=log_filepath)

    # 데이터베이스 처리
    from photolog.database import DBManager
    db_filepath = os.path.join(photolog_app.root_path,
                               photolog_app.config['DB_FILE_PATH'])

    db_url = photolog_app.config['DB_URL']
    DBManager.init(db_url, eval(photolog_app.config['DB_LOG_FLAG']))
    DBManager.init_db()

    # 뷰 함수 모듈은 어플리케이션 객채 생성하고 블루프린트 등록전에
    # 뷰 함수가 있는 모듈을 임포트해야 해당 뷰 함수들을 인식할수 있음
    from photolog.controller import login
    from photolog.controller import photo_show
    from photolog.controller import photo_upload
    from photolog.controller import register_user
    from photolog.controller import twitter

    # SessionInterface 설정 Redis
    from photolog.cache_session import SimpleCacheSessionInterface
    photolog_app.session_interface = SimpleCacheSessionInterface()

    # 공통적으로 적용할 HTTP 404, 500 에러 핸들러를 설정
    photolog_app.error_handler_spec[None][404] = not_found
    photolog_app.error_handler_spec[None][500] = server_error

    # 페이징 처리를 위한 템플릿 함수
    photolog_app.jinja_env.globals['url_for_other_page'] = url_foer_other_page

    return photolog_app