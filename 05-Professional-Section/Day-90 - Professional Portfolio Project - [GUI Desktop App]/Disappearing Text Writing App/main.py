from flask import Flask, render_template, request, jsonify, session
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

# In a real application, you'd use a database
# For simplicity, we'll store user sessions in memory (not suitable for production)
user_sessions = {}


@app.route('/')
def index():
    # Initialize a session for the user
    if 'user_id' not in session:
        session['user_id'] = secrets.token_urlsafe(16)
        user_sessions[session['user_id']] = {
            'last_activity': datetime.now(),
            'content': ''
        }
    return render_template('index.html')


@app.route('/save', methods=['POST'])
def save_content():
    if 'user_id' not in session:
        return jsonify({'error': 'No active session'}), 400

    user_id = session['user_id']
    content = request.json.get('content', '')

    # Update the user's content and last activity time
    if user_id in user_sessions:
        user_sessions[user_id]['content'] = content
        user_sessions[user_id]['last_activity'] = datetime.now()

    return jsonify({'status': 'success'})


@app.route('/check_activity')
def check_activity():
    if 'user_id' not in session:
        return jsonify({'active': False, 'content': ''})

    user_id = session['user_id']

    if user_id not in user_sessions:
        return jsonify({'active': False, 'content': ''})

    # Check if user has been inactive for more than 5 seconds
    last_activity = user_sessions[user_id]['last_activity']
    inactive_time = (datetime.now() - last_activity).total_seconds()

    if inactive_time > 5:  # 5 seconds of inactivity
        # Delete content due to inactivity
        user_sessions[user_id]['content'] = ''
        return jsonify({'active': False, 'content': ''})

    return jsonify({
        'active': True,
        'content': user_sessions[user_id]['content'],
        'inactive_time': inactive_time
    })


@app.route('/download')
def download_content():
    if 'user_id' not in session:
        return "No content to download", 400

    user_id = session['user_id']
    content = user_sessions.get(user_id, {}).get('content', '')

    # Create a response with the content as a file attachment
    response = app.response_class(
        response=content,
        status=200,
        mimetype='text/plain'
    )
    response.headers.set('Content-Disposition', 'attachment', filename='dangerous_writing.txt')
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5000)
