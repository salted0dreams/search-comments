from flask import Flask, jsonify, request
import urllib.request, json

app = Flask(__name__)

BASE_URL = 'https://app.ylytic.com/ylytic/test'

@app.route('/greetings')
def greetings():
    return 'May the force be with you!'

@app.route('/getdata')
def getdata():
    response = urllib.request.urlopen(BASE_URL)
    data = json.loads(response.read())
    return jsonify(data)

@app.route("/search", methods=["GET"])
def search_comments():
    response = urllib.request.urlopen(BASE_URL)
    response_data = response.read().decode('utf-8')  # Decode response data
    comments = json.loads(response_data)  # Load JSON data
    comments_array = comments["comments"]

    search_author = request.args.get("search_author")
    at_from = request.args.get("at_from")
    at_to = request.args.get("at_to")
    like_from = int(request.args.get("like_from", 0))
    like_to = int(request.args.get("like_to", 9999999999))  # Use a large number as an upper bound
    reply_from = int(request.args.get("reply_from", 0))
    reply_to = int(request.args.get("reply_to", 9999999999))  # Use a large number as an upper bound
    search_text = request.args.get("search_text")

    filtered_comments = []
    for comment in comments_array:
        if search_author and search_author not in comment["author"]:
            continue
        if at_from and comment["at"].startswith(at_from):
            continue
        if at_to and comment["at"].startswith(at_to):
            continue
        comment_like = int(comment["like"])  # Convert comment["like"] to an integer
        comment_reply = int(comment["reply"])  # Convert comment["reply"] to an integer
        if comment_like < like_from or comment_like > like_to:
            continue
        if comment_reply < reply_from or comment_reply > reply_to:
            continue
        if search_text and search_text not in comment["text"]:
            continue
        filtered_comments.append(comment)

    return jsonify(filtered_comments)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
