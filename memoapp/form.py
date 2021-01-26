from django.contrib.auth.models import User
from django.forms import ModelForm, forms, CheckboxInput, Textarea, TextInput, EmailInput, PasswordInput

from memoapp.models import Memos


class Postform(ModelForm):
    class Meta:
        model = Memos
        fields = ['title', 'text', 'priority']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control',}),
            'text': Textarea(attrs={'class': 'form-control', 'placeholder':'230자 이내로 입력 가능합니다.'}),
            'priority': CheckboxInput(attrs={'type' : 'checkbox'}),
        }
        labels = {
            'title': '제목',
            'text': '내용',
            'priority': '중요',
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': '15자 이내로 입력 가능합니다.'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': '닉네임',
            'eamil': '이메일',
            'password': '비밀번호',
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['maxlength'] = 15


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
