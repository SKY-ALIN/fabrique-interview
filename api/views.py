from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Pool, Question
from .serializers import PoolSerializer, PoolFullSerializer, UserAnswerSerializer

class PoolViewSet(APIView):
    """Pools list view."""

    def get(self, request):
        pools = Pool.objects.filter(end__gte=timezone.now())
        serializer = PoolSerializer(pools, many=True)
        return Response(serializer.data)


class PoolView(APIView):
    """Get more information about some pool (questions and their options)."""

    def get(self, request, pk):
        try:
            pool = Pool.objects.get(pk=pk)
        except Pool.DoesNotExist:
            return Response(status=404)

        serializer = PoolFullSerializer(pool)
        return Response(serializer.data)


class AnswerView(APIView):
    """Answers view."""

    def get(self, request):
        """Get user's pools and answers."""

        # Reject if user is not authorized
        if request.user.is_anonymous:
            return Response(status=403)

        pools = Pool.objects.filter(questions__users_answers__user_id=request.user.id)
        pools_serializer = PoolFullSerializer(set(pools), many=True)

        user_answers = request.user.useranswer_set.all()
        answer_serializer = UserAnswerSerializer(user_answers, many=True)

        data = {
            "answers": answer_serializer.data,
            "pools": pools_serializer.data,
        }
        return Response(data)


    def post(self, request):
        """Post a answer."""

        serializer = UserAnswerSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = serializer.validated_data.get('user')
        if user and user.id != request.user.id:
            return Response(status=403)

        question = serializer.validated_data.get('question')

        # Example: {"question": 1, "text": "LOL"}
        if question.type == Question.TEXT_TYPE:
            if not serializer.validated_data.get('text'):
                return Response(status=400)

        # Example: {"question": 2, "answer_options": [1]}
        elif question.type == Question.SINGLE_TYPE:
            if len(serializer.validated_data.get('answer_options')) != 1:
                return Response(status=400)

        # Example: {"question": 3, "answer_options": [3, 4]}
        elif question.type == Question.MULTIPLE_TYPE:
            if not serializer.validated_data.get('answer_options'):
                return Response(status=400)

        serializer.save()
        return Response(serializer.data, status=200)
