

from rest_framework import serializers

class TicketSerializer(serializers.Serializer):
    project_key = serializers.CharField(max_length=10)
    summary = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1000)
    issue_type = serializers.CharField(max_length=20)

class TaskSerializer(serializers.Serializer):
    issue_key = serializers.CharField(max_length=20)
    summary = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1000)

class IssueKeySerializer(serializers.Serializer):
    issue_key = serializers.CharField(max_length=20)
