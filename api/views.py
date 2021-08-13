from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from quiz.models import Test, Question
from api.serializers import TestSerializer, QuestionSerializer, TestTotalSerializer
from rest_framework import mixins, generics, filters


class TestViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    # queryset = Test.objects.all()
    serializer_class = TestSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title', 'created_at']
    ordering = ['created_at']

    def get_queryset(self):
        queryset = Test.objects.all()
        title = self.request.query_params.get('title')
        total_users = self.request.query_params.get('total_users')
        if total_users is not None:
            queryset = queryset.filter(total_users=total_users)
        if title is not None:
            queryset = queryset.filter(title=title)
        return queryset

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


class TestRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class QuestionRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



