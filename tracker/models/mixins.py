from tracker.extensions import db


class SaveDeleteMixin(object):
	is_deleted = db.Column(db.Boolean, default=False)

	def delete(self):
		self.is_deleted = True
		db.session.add(self)
		db.session.commit()

	def undelete(self):
		self.is_deleted = False
		db.session.add(self)
		db.session.commit()

	def save(self):
		db.session.add(self)
		db.session.commit()


class SerializationMixin(object):

	def to_dict(self):
		return self.__serializer__(self).data
