from django import forms


class PostCreateForm(forms.Form):
    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control-file',
                'multiple': True,
            }
        )
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def save(self):
        pass


class CommentCreateForm(forms.Form):
    content = forms.CharField(
        max_length=10,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 2,
            }
        )
    )

    def save(self, post, author):
        return post.postcomment_set.create(
            author=author,
            content=self.cleaned_data['content'],
        )