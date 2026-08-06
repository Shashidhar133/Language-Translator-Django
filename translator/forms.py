from django import forms
from .models import Translation


LANGUAGE_CHOICES = [
    ("en", "English"),
    ("es", "Spanish"),
    ("fr", "French"),
    ("de", "German"),
    ("hi", "Hindi"),
    ("te", "Telugu"),
]


class TranslationForm(forms.Form):

    text = forms.CharField(
        label="Text to Translate",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Enter text here..."
            }
        )
    )

    source_language = forms.ChoiceField(
        label="Source Language",
        choices=LANGUAGE_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    target_language = forms.ChoiceField(
        label="Target Language",
        choices=LANGUAGE_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()

        source = cleaned_data.get("source_language")
        target = cleaned_data.get("target_language")

        if source == target:
            raise forms.ValidationError(
                "Source and target languages must be different."
            )

        return cleaned_data


class TranslationNoteForm(forms.ModelForm):

    class Meta:
        model = Translation
        fields = ["notes"]

        widgets = {
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write your notes..."
                }
            )
        }