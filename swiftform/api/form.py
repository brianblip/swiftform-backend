from flask import Blueprint, request, jsonify
from swiftform.models import Form
from swiftform.app import db
from flask_jwt_extended import jwt_required, current_user

form = Blueprint('form', __name__)

@form.route('/api/v1/forms', methods=['POST'])
@jwt_required()
def create_form():
    data = request.json

     # Get the user ID of the currently logged-in user
    user_id = current_user.id

    new_form = Form(
        name=data['name'],
        description=data['description'],
        user_id=user_id,
        created_at=data['created_at'],
        updated_at=data['updated_at']
    )

    db.session.add(new_form)
    db.session.commit()
    return jsonify({'message': 'Form created successfully'}), 201


@form.route('/api/v1/forms/<int:form_id>', methods=['GET'])
@jwt_required()
def get_form(form_id):
    form = Form.query.get(form_id)
    if form is None:
        return jsonify({'error': 'Form not found'}), 404
    
    user_id = current_user.id

    # Check if the logged-in user is the creator of the form
    if form.user_id != user_id:
        return jsonify({'error': 'You are not authorized to access this form'}), 403
    
    form_data = {
        'id': form.id,
        'name': form.name,
        'description': form.description,
        'user_id': form.user_id,
        'created_at': form.created_at,
        'updated_at': form.updated_at
    }
    return jsonify(form_data), 200

@form.route('/api/v1/forms/<int:form_id>', methods=['PUT'])
@jwt_required()
def update_form(form_id):
    form = Form.query.get(form_id)
    if form is None:
        return jsonify({'error': 'Form not found'}), 404

    user_id = current_user.id
    
    if form.user_id != user_id:
        return jsonify({'error': 'You are not authorized to update this form'}), 403

    data = request.json
    form.name = data.get('name', form.name)
    form.description = data.get('description', form.description)
    form.updated_at = data.get('updated_at', form.updated_at)

    db.session.commit()
    return jsonify({'message': 'Form updated successfully'}), 200

@form.route('/api/v1/forms/<int:form_id>', methods=['DELETE'])
@jwt_required()
def delete_form(form_id):
    form = Form.query.get(form_id)
    if form is None:
        return jsonify({'error': 'Form not found'}), 404
 
    user_id = current_user.id

    if form.user_id != user_id:
        return jsonify({'error': 'You are not authorized to delete this form'}), 403

    db.session.delete(form)
    db.session.commit()
    return jsonify({'message': 'Form deleted successfully'}), 200