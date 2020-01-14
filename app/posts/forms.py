from django import forms


class PostCreateForm(forms.Form):
    """
    이 Form에 들어갈 입력요소
        Image(File)
        Text
    """
    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True,
            }
        )
    )
    text = forms.CharField()

    def save(self):
        pass


class CommentCreateForm(forms.Form):
    content = forms.CharField(
        max_length=10,
        widget=forms.Textarea()
    )

    def save(self, post, author):
        return post.postcomment_set.create(
            author=author,
            content=self.cleaned_data['content'],
        )
