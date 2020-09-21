from rest_framework import serializers

from .models import Pool, Question, AnswerOption, UserAnswer


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = "__all__"


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ('id', 'text')


class QuestionFullSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        exclude = ('pool', )


class PoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pool
        fields = "__all__"


class PoolFullSerializer(serializers.ModelSerializer):
    questions = QuestionFullSerializer(read_only=True, many=True)

    class Meta:
        model = Pool
        fields = "__all__"
