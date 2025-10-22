from bson import ObjectId
from mongoengine import (
    Document,
    StringField,
    EmailField,
    ListField,
    BooleanField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    DateTimeField,
    ReferenceField,
)
import datetime


class QueryAnswer(EmbeddedDocument):
    query = StringField(required=True)
    answers = ListField(StringField(), required=True)


class QueriesGot(EmbeddedDocument):
    userId = ReferenceField("User")  # <-- reference to the User document (ObjectId)
    queryId = StringField()
    queryText = StringField(required=True)
    answered = BooleanField(default=False)
    response = StringField()


class User(Document):
    email = EmailField(required=True, unique=True)
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(required=True)  # "learner" or "moderator"
    skills = ListField(StringField(), required=True)
    queries = ListField(EmbeddedDocumentField(QueryAnswer))
    queriesGot = ListField(EmbeddedDocumentField(QueriesGot))
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {"collection": "users"}  # equivalent to mongoose.model('queries')
