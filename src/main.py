import helper.api as api

def main():
    app = api.FlaskAPIServer().get_app()
    return app

if __name__ == '__main__':
    main_app = main()
    main_app.run(host='127.0.0.1', port=58769, debug=True)