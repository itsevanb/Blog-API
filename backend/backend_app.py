from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

posts = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    #add sorting functionality
    sort = request.args.get('sort')
    direction = request.args.get('drection')

    if sort is not None and sort not in ["title", "content"]:
        return jsonify({"error": "Invalid sort parameter"}), 400
    
    if direction is not None and direction not in ["asc", "desc"]:
        return jsonify({"error": "Invalid direction parameter"}), 400
    
    if sort is not None:
        posts_copy = posts.copy()
        posts_copy.sort(key=lambda x: x[sort])
        if direction == "desc":
            posts_copy.reverse()
        return jsonify(posts_copy), 200
    return jsonify(posts), 200

#Add a new post
@app.route('/api/posts', methods=['POST'])
def add_post():
    if request.is_json:
        new_post = request.get_json()
        new_post['id'] = max(post['id'] for post in posts) + 1 #unique id per post
        posts.append(new_post)
        return jsonify(posts), 201
    return jsonify({"error": "Request must be JSON"}), 400

#Delete a post
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = next((post for post in posts if post['id'] == post_id), None) #Find post by ID
    if post:
        posts.remove(post)
        return 'Post deleted', 204
    return 'Post not found', 404

#Update a post
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = next((post for post in posts if post['id'] == post_id), None) #Find post by ID
    if post and request.is_json:
        updated_post = request.get_json()
        post.update(updated_post) #Update the post with the new data
        return jsonify(post), 200
    return 'Post not found or request was not JSON', 400 #Bad request

#Search for posts by title
@app.route('/api/posts/search/<string:title>', methods=['GET'])
def search_posts(title):
    matching_posts = [post for post in posts if title in post['title']] #Find all posts that contain the search string
    return (jsonify(matching_posts), 200) if matching_posts else (jsonify(matching_posts), 404) #Return 200 if posts were found, 404 if not

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
