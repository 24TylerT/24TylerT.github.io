from website import create_app
from replit import web

app = create_app()

if __name__ == '__main__':
    #app.run(debug=True)
    
    web.run(app, debug=False)
    #app.run(host='127.0.0.1', port=5500)