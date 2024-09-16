from rest_framework import serializers

class ExcelUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.xlsx'):
            raise serializers.ValidationError("Chỉ chấp nhận file Excel (.xlsx)")
        return value