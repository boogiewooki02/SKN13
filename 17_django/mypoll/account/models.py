from django.db import models
from django.contrib.auth.models import AbstractUser

# User 모델 등록
## AbstractUser 클래스를 상속받아서 사용자 모델을 정의

class User(AbstractUser):
    # username/password를 제외한 나머지 필드들을 정의
    name = models.CharField(
        verbose_name="이름", # Form관련 설정. ModelForm을 만들 경우 from관련 설정을 Model field에 할 수 있다.
        max_length=50, # varchar(50)
    )
    email = models.EmailField(
        verbose_name="이메일",
        max_length=100, # varchar(100)
    )
    birthday = models.DateField(
        verbose_name="생일",
        null=True, # null 허용
        blank=True, # 입력폼 설정 - 빈 값 허용(default: False - required)
    )

    def __str__(self):
        return f"{self.username} - {self.name}"

