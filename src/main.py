import helper.api as api
import jwt


def main():
    server = api.FlaskAPIServer()
    app = server.get_app()
    print(f"JWT Token: {server.token}")
    return app


if __name__ == '__main__':
    main_app = main()
    main_app.run(host='127.0.0.1', port=58769, debug=True)
