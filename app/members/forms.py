from django import forms


class LoginForm(forms.Form):
    # 로그인 시 사용

    pass


class SignupForm(forms.Form):
    def save(self):
        """
        Form으로 전달받은 데이터를 사용해서
        새로운 User를 생성하고 리턴

        username과 email검증로직도 이 안에 넣기
        """
        pass
