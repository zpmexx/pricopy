from rest_framework import serializers
from news.models import News

class GetNewsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = News
        fields = ['id','title','short_content','content','slug','image']
    
class CreateNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        # fields = ['title','short_content','content','image']
        fields = ['title','short_content','content','slug']
        
    def create(self, validated_data):
        return News.objects.create(**validated_data)

