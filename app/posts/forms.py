from django import forms


class PostCreateForm(forms.Form):
    """
    이 Form에 들어갈 입력요소
        Image(File)
        Text
    """
    image = forms.ImageField(label='image')
    text = forms.CharField(max_length=100)
