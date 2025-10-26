from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Hello from Vercel!', 'status': 'API working'}

@app.route('/health')
def health():
    return {'status': 'healthy', 'service': 'note-taking-app'}

if __name__ == '__main__':
    app.run()