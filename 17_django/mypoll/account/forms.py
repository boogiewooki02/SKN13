from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # User모델의 model field를 이용해서 Form field를 구성
        # fields = "__all__"  # User모델의 모든 필드를 Form field로 사용
        fields = ["username", "password1", "password2", "name", "email", "birthday"]  # 사용할 필드만 지정
        # exclude = ('password1', 'password2')  # 지정한 필드는 제외 (fields와 exclude는 함께 사용하지 못함)
        
        # Form Field의 input type 변경
        ## birthday input type=text ==> input type=date
        # key: Form Field name, value: Widget 객체
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            # 'name': forms.PasswordInput()
        }

    # 검증
    # Form이나 ModelForm에서 하는 기본 검증
    # - blank=False: 필수 입력
    # - 숫자 입력: 숫자인지 검증
    # - Emmail 입력: 이메일 형식인지 검증
    # - Date 입력: 날짜 형식인지 검증

    # 검증 메소드 추가 - 도메인 특화 검증을 할 경우 정의한다.
    # - clean(): Form의 모든 필드에 대한 검증을 수행한다.
    # - clean_<field_name>(): 특정 필드에 대한 검증을 수행한다.
    # 검증시 문제가 발생하면 ValidationError 예외를 발생시킨다.
