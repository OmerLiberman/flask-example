import os

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class VideoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	views = db.Column(db.Integer, nullable=False)
	likes = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"Video(name = {VideoModel.name}, " \
			   f"views = {VideoModel.views}, likes = {VideoModel.likes}"


# db.create_all()


video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, required=True, help="name of the video")
video_put_args.add_argument("likes", type=int, required=True, help="likes of the video")
video_put_args.add_argument("views", type=int, required=True, help="views of the video")

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="name of the video")
video_update_args.add_argument("likes", type=int, help="likes of the video")
video_update_args.add_argument("views", type=int, help="views of the video")

resource_fields = {
	"id": fields.Integer,
	"name": fields.String,
	"views": fields.Integer,
	"likes": fields.Integer
}


class Video(Resource):
	@marshal_with(resource_fields)
	def get(self, video_id):
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="ID does not exist.")
		return result

	@marshal_with(resource_fields)
	def put(self, video_id):
		args = video_put_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		if result:
			abort(409, message="Video taken..")
		# else:
		video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
		db.session.add(video)
		db.session.commit()
		return video, 201  # 201 - created.

	@marshal_with(resource_fields)
	def patch(self, video_id):  # like UPDATE
		args = video_update_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="ID does not exist.")

		result.name = args["name"] if args["name"] is not None else result.name
		result.views = args["views"] if args["views"] is not None else result.views
		result.likes = args["likes"] if args["likes"] is not None else result.likes

		db.session.commit()
		return result, 200

	@marshal_with(resource_fields)
	def delete(self, video_id):
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="ID does not exist.")
		db.session.delete(result)
		db.session.commit()
		return {}, 204


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == '__main__':
	app.run(debug=True)
