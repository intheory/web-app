from mongoengine import Document, DateTimeField, DictField, IntField, ObjectIdField, StringField, EmbeddedDocument, EmbeddedDocumentField, ListField, BooleanField, ReferenceField

class Coupon(Document):
	meta = {"collection":"Coupons", 'allow_inheritance': True}
	code = StringField(required=True)
	discount = IntField(required=True)
	expiration_date = DateTimeField(required=True)
	redeemed = BooleanField(required=True, default=False)
