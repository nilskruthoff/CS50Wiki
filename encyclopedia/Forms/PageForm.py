from django import forms


class PageForm(forms.Form):
    title = forms.CharField(label="Page Title")
    content = forms.CharField(label="Page Content", widget=forms.Textarea)
