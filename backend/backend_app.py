from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


def open_json_file():
    filepath = 'posts.json'
    with open(filepath, "r") as handle:
        return json.load(handle)


POSTS = open_json_file()


def update_json_file(POSTS):
    filepath = 'posts.json'
    with open(filepath, "w") as handle:
        json.dump(POSTS, handle)


def new_post_error(new_post):
    """tests new_post data and creates a dict with errors"""
    error = {}
    if 'title' not in new_post:
        error['error_title'] = 'Missing title in json'
    elif len(new_post['title']) < 2 or new_post['title'] == None:
        error['error_title'] = 'Short or empty title'
    if 'content' not in new_post:
        error['error_content'] = 'Missing content in json'
    elif len(new_post['content']) < 2 or new_post['content'] == None:
        error['error_content'] = 'Short or empty content'
    if 'author' not in new_post:
        error['error_content'] = 'Missing author in json'
    if len(error) == 0:
        return None
    else:
        return error


@app.route('/api/posts', methods=['POST'])
def add_post():
    """ Post methos to add new post, if error occurs responses with a json error dict
  #ID is taken from the last POSTS[id] + 1 or equals to 1 if POSTS list is empty"""
    new_post = request.get_json()
    error = new_post_error(new_post)
    if error != None:
        print(error)
        return jsonify(new_post_error(new_post)), 400
    print(new_post['title'])
    print('title' in new_post)
    if len(POSTS) == 0:
        new_id = 1
    else:
        new_id = max(post['id'] for post in POSTS) + 1
    new_post['id'] = new_id
    new_post['date'] = datetime.today().strftime('%Y-%m-%d')
    POSTS.append(new_post)
    update_json_file(POSTS)
    return jsonify(new_post), 201


def sort_posts(sort, direction):
    """
  """
    if direction == "desc":
        asc = True
    else:
        asc = False
    if sort == "date":
        sorted_posts = sorted(POSTS, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=asc)
    elif sort is not None:
        sorted_posts = sorted(POSTS, key=lambda x: x[sort].lower(), reverse=asc)
    else:
        sorted_posts = sorted(POSTS, key=lambda x: x['id'], reverse=asc)
    return sorted_posts


@app.route('/api/posts', methods=['GET'])
def get_posts():
    args = request.args
    sort = args.get("sort", default=None, type=str)
    direction = args.get("direction", default=None, type=str)
    sorted_list = sort_posts(sort, direction)
    # pagination
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    start_index = (page - 1) * limit
    end_index = start_index + limit
    return jsonify(sorted_list[start_index:end_index])


def find_post_by_id(post_id):
    """ Find the post with the id `post_id`.
  If there is no post with this id, return None. """
    post = list(filter(lambda x: x['id'] == post_id, POSTS))
    if len(post) == 0:
        return None
    else:
        return post[0]


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """Find the posts with the given ID (using find_post_by_id), # If the post wasn't found, return a 404 error"""
    post = find_post_by_id(id)
    if post is None:
        return '', 404
    else:
        POSTS.remove(post)
        update_json_file(POSTS)
        message_to_show = f'Post with id {id} has been deleted successfully.'
        return jsonify({'message': message_to_show}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """ Find the post with the given ID (using find_post_by_id),  If the post wasn't found, return a 404 error
    Updates POSTS with new data"""
    post = find_post_by_id(id)
    if post is None:
        return jsonify({'message': 'Post not found'}), 404
    new_data = request.get_json()
    post_index = POSTS.index(post)
    if "title" in new_data:
        POSTS[post_index]['title'] = new_data['title']
    if "content" in new_data:
        POSTS[post_index]['content'] = new_data['content']
    if "author" in new_data:
        POSTS[post_index]['author'] = new_data['author']
    if "date" not in new_data:
        POSTS[post_index]['date'] = datetime.today().strftime('%Y-%m-%d')
    update_json_file(POSTS)
    return jsonify(POSTS[post_index]), 200


def search_post(title, content, author, date):
    """Function to search data in POSTS by title or content"""
    search_result = POSTS
    if title is not None:
        search_result = list(filter(lambda x: title.lower() in x['title'].lower(), search_result))
    if content is not None:
        search_result = list(filter(lambda x: content.lower() in x['content'].lower(), search_result))
    if author is not None:
        search_result = list(filter(lambda x: author.lower() in x['author'].lower(), search_result))
    if date is not None:
        search_result = list(filter(lambda x: date in x['date'], search_result))
    return search_result


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Search in POSTS by using search_post(), the data to search from query parameters
  If nothing found return empty json"""
    args = request.args
    title = args.get("title", default=None, type=str)
    content = args.get("content", default=None, type=str)
    author = args.get("author", default=None, type=str)
    date = args.get("date", default=None, type=str)
    result = search_post(title, content, author, date)
    return jsonify(result), 200


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
