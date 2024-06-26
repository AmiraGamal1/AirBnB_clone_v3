#!/usr/bin/python3
"""A module that contains the places_reviews view for the API.
"""
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_reviews(place_id=None, review_id=None):
    """The method handler for the reviews endpoint.
    """
    handler_dict = {
        'GET': get_review,
        'DELETE': remove_review,
        'POST': add_review,
        'PUT': update_review
    }
    if request.method in handler_dict:
        return handler_dict[request.method](place_id, review_id)
    else:
        raise MethodNotAllowed(list(handler_dict.keys()))


def get_review(place_id=None, review_id=None):
    """Gets the review with the given id or all reviews in
       the place with the given id.
    """
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            reviews = []
            for review in place.reviews:
                reviews.append(review.to_dict())
            return jsonify(reviews)
    elif review_id:
        review = storage.get(Review, review_id)
        if review:
            return jsonify(review.to_dict())
    raise NotFound()


def remove_review(place_id=None, review_id=None):
    """Removes a review with the given id.
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_review(place_id=None, review_id=None):
    """Adds a new review.
    """
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound()
    a_data = request.get_json()
    if type(a_data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'user_id' not in a_data:
        raise BadRequest(description='Missing user_id')
    user = storage.get(User, a_data['user_id'])
    if not user:
        raise NotFound()
    if 'text' not in a_data:
        raise BadRequest(description='Missing text')
    a_data['place_id'] = place_id
    new_review = Review(**a_data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


def update_review(place_id=None, review_id=None):
    """Updates the review with the given id.
    """
    x_keys = ('id', 'user_id', 'place_id', 'created_at', 'updated_at')
    if review_id:
        review = storage.get(Review, review_id)
        if review:
            a_data = request.get_json()
            if type(a_data) is not dict:
                raise BadRequest(description='Not a JSON')
            for k, v in a_data.items():
                if k not in x_keys:
                    setattr(review, k, v)
            review.save()
            return jsonify(review.to_dict()), 200
    raise NotFound()
