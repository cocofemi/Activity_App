from rest_framework import serializers

from activity.models import Activity

class ActivitySerializer(serializers.ModelSerializer):
	class Meta:
		model = Activity
		fields = ('author','name', 'description', 'image', 'category','start_date', 'end_date', )