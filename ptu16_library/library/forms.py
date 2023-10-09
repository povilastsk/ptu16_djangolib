from django import forms
from . import models


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = models.BookReview
        fields = ('content', 'book', 'reviewer')
        widgets = {
            'book': forms.HiddenInput(),
            'reviewer': forms.HiddenInput(),
        }
        labels = {
            'content': '',
        }


class BookInstanceForm(forms.ModelForm):
    class Meta:
        model = models.BookInstance
        fields = ('book', 'due_back', 'status', 'reader' )
        widgets = {
            'book': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'reader': forms.HiddenInput(),
        }
        labels = {
            'due_back': 'until'
        }