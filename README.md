## RESTful Blog API
This is a RESTful Flask-based API for managing blog posts. It provides endpoints for creating, retrieving, updating, and deleting blog posts. The application uses a JSON file (posts.json) to store post data.

## Endpoints
1. Add a New Post
Endpoint: POST /api/posts
Payload: JSON data with title, content, and author fields.
Response: Returns the created post with a unique identifier (id) and creation date.
2. Get Paginated List of Posts
Endpoint: GET /api/posts
Query Parameters:
sort: Field to sort posts by (id, title, content, author, date).
direction: Sort direction (asc or desc).
page: Page number for pagination.
limit: Number of posts per page.
Response: Returns a paginated list of posts based on the provided query parameters.
3. Delete a Post
Endpoint: DELETE /api/posts/<int:id>
Response: Deletes the post with the specified id and returns a success message.
4. Update a Post
Endpoint: PUT /api/posts/<int:id>
Payload: JSON data with fields to update (title, content, author).
Response: Updates the specified post and returns the updated post.
5. Search Posts
Endpoint: GET /api/posts/search
# Query Parameters:
title: Search posts by title.
content: Search posts by content.
author: Search posts by author.
date: Search posts by date.
# Response: Returns a list of posts that match the search criteria.
# Error Handling
404 Not Found:
Returned when an endpoint or resource is not found.
405 Method Not Allowed:
Returned when an unsupported HTTP method is used for an endpoint.
