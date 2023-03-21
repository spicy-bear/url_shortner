from flask import Flask, request, redirect, render_template, url_for
import redis
import shortuuid

app = Flask(__name__)
db = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        if not original_url.startswith('http'):
            original_url = 'http://' + original_url
        short_id = shortuuid.uuid(name=original_url)[:6]
        db.set(short_id, original_url)
        short_url = request.host_url + short_id
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')

@app.route('/<short_id>')
def redirect_url(short_id):
    original_url = db.get(short_id)
    if original_url is None:
        return render_template('error.html'), 404
    return redirect(original_url.decode('utf-8'))

#if __name__ == '__main__':
#    app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
