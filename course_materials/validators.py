from rest_framework.serializers import ValidationError


def validate_youtube_link(value):
    if "https://www.youtube.com/" not in value:
        raise ValidationError("can post only to youtube")