from django import forms

class SearchForm(forms.Form):
    prompt = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your prompt', 'class' : 'typing-input', 'rows': 1, 'id':'searchInput', 'autocomplete': 'off'}))
