from django import forms
from .models import Comment

# class EmailPostForm(forms.Form):
#     name = forms.CharField(max_length=25)
#     email = forms.EmailField()
#     to=forms.EmailField()
#     comments=forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')
        labels={
            'body':'Izoh:'
        }
        widgets={
            'name':forms.TextInput(attrs={'placeholder':'Name:'}),
            'email':forms.EmailInput(attrs={'placeholder':'Email'}),
            'body':forms.Textarea(attrs={'placeholder':'Izoh maydoni:'})
        }
class SearchForm(forms.Form):
    query=forms.CharField()