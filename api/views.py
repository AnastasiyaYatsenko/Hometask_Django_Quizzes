from rest_framework import viewsets
from quiz.models import Test, Question
from api.serializers import TestSerializer, QuestionSerializer, TestTotalSerializer
from rest_framework import mixins, generics


class TestViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class QuestionViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TestTotalViewSet(mixins.ListModelMixin,
                       generics.GenericAPIView):
    queryset = Test.objects.order_by('-total_users')
    serializer_class = TestTotalSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TestFirstThreeViewSet(mixins.ListModelMixin,
                            generics.GenericAPIView):
    queryset = Test.objects.order_by('-total_users')[:3]
    serializer_class = TestTotalSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
