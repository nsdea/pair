"""A website for sharing data between devices using a code."""

import os
import time
import random
import flask
import qrcode

HOST = 'http://192.168.178.172:2121'

app = flask.Flask(__name__) #pylint: disable=invalid-name

connections = {} #pylint: disable=invalid-name

@app.route('/', methods=['GET'])
def index():
    """Main Page"""
    return flask.render_template('index.html')

def remove_image(code: int):
    """Removes an images from the temp using a specified code."""
    time.sleep(60)
    os.remove(f'src/static/qrcodes/{code}.png')

@app.route('/new', methods=['POST'])
def new():
    """Page for creating a new code."""
    global connections #pylint: disable=invalid-name,global-statement

    random_code = random.randint(1000, 9999)
    message = flask.request.form.to_dict()['message']
    connections[random_code] = message

    qr = qrcode.QRCode( #pylint: disable=invalid-name
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f'{HOST}/view?code={random_code}')
    qr.make(fit=True)

    img = qr.make_image(fill_color="white", back_color="black")
    path = f'qrcodes/{random_code}.png'
    img.save(f'src/static/{path}')

    return flask.render_template('new.html', code=random_code, message=message, image=path)

@app.route('/view', methods=['POST', 'GET'])
def view():
    """Page for viewing a code and its message."""
    global connections # pylint: disable=invalid-name,global-statement

    code = flask.request.form.to_dict().get('code')

    if flask.request.method == 'GET':
        code = flask.request.args.get('code')

    message = connections[int(code)]

    if '://' in message:
        return flask.redirect(message)

    return flask.render_template('view.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2121, debug=True)
