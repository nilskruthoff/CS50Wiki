from django import forms


class PageForm(forms.Form):
    title = forms.CharField(label="Page Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label="Page Content", widget=forms.Textarea(attrs={'class': 'form-control'}))
