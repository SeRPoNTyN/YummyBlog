from django import forms
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentUnderPost
        # fields = "__all__"
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={'class': 'form-control', "rows": 5}),
        }
