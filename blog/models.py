from turtle import title
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Length, Replace
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    tags = models.CharField(max_length=255)
    timestamp = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title}"

    @classmethod
    def get_relevance_sorted_posts(self, type, query=""):
        # Define your updated relevance calculation logic here
        relevance_expression = (
            # Count the number of tags
            Length('title') + Length(F('tags')) - \
            Length(Replace(F('tags'), Value(','), Value('')))
        )

        # Annotate the queryset with the relevance score
        queryset = self.objects.annotate(relevance_score=relevance_expression)

        if (query):
            if (type == "title"):
                queryset = queryset.filter(title__icontains=query)
            else:
                queryset = queryset.filter(tags__icontains=query)

        # Order the queryset by the relevance score in descending order
        queryset = queryset.order_by('-relevance_score')

        return queryset
