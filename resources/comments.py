from flask_restful import Resource,reqparse
from models.comments import CommentModel
from flask_jwt_extended import jwt_required, current_user
comment_parser = reqparse.RequestParser()
comment_parser.add_argument('content',
        type=str,
        required=True,
        help="Required Filed"
)
comment_parser.add_argument('likes', type=int)
comment_parser.add_argument('created_date')
comment_parser.add_argument('post_id')
comment_parser.add_argument('user_id')

class CreateComment(Resource):
    @jwt_required()
    def post(self):
        data = comment_parser.parse_args()
        comment = CommentModel(**data)
        comment.save_to_db()
        return {"message": "Comment Created"}, 201

class Comment(Resource):
    @classmethod
    @jwt_required()
    def get(cls,comment_id):
        comment = CommentModel.find_by_id(comment_id)
        if not comment:
            return {'message': 'Comment Not Found'}, 404
        return comment.json()
    @jwt_required()
    def delete(cls, comment_id):
        comment = CommentModel.find_by_id(comment_id)
        
        if comment.user_id != current_user.id:
            return {'message': 'This Action is Unauthorized Bro'}, 401
        comment.delete_from_db()
        return {'message': 'Comment Deleted'}
    @jwt_required()
    def put(cls, comment_id):
        data = comment_parser.parse_args()
        comment = CommentModel.find_by_id(comment_id)
        if comment.user_id != current_user.id:
            return {'message': 'This Action is Unauthorized Bro'}, 401
        comment.content = data['content']
        comment.save_to_db()
        return comment.json()