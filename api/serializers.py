from quiz.models import Test, Question
from rest_framework import serializers


class TestSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.SerializerMethodField()
    title = serializers.CharField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)

    def get_name(self, name):
        return f'Name of Test: {name}'

    class Meta:
        model = Test
        fields = ['name', 'title', 'description', 'created_at']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class TestTotalSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.SerializerMethodField()
    total_users = serializers.IntegerField()

    def get_name(self, name):
        return f'Name of Test: {name}'

    class Meta:
        model = Test
        fields = ['name', 'total_users']
