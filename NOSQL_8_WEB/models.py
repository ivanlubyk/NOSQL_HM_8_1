from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField


uri = "mongodb+srv://web12_user:641641@cluster12.bopqszz.mongodb.net/?retryWrites=true&w=majority"
class Author(Document):
    fullname = StringField(required=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()