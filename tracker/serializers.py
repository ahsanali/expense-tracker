from marshmallow import Serializer, fields
 
class UserSerializer(Serializer):
    class Meta:
        fields = ("id", "email","name","phone","created_time","age","sex_code")
 
class ExpenseSerializer(Serializer):
    user = fields.Nested(UserSerializer)
 
    class Meta:
        fields = ("id", "description", "expense_time", "amount")

class CommentSerializer(Serializer):
	user = fields.Nested(UserSerializer)

	class Meta:
		fields = ("id", "pub_date", "text")