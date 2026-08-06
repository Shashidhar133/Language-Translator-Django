from django.db import models
from django.contrib.auth.models import User


LANGUAGE_CHOICES = [
    ("en", "English"),
    ("es", "Spanish"),
    ("fr", "French"),
    ("de", "German"),
    ("hi", "Hindi"),
    ("te", "Telugu"),
]


user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="translations"
)

class Translation(models.Model):

    original_text = models.TextField()

    translated_text = models.TextField()

    source_language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
    )

    target_language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_text[:30]}..."