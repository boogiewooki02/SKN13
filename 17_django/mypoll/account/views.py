from django.shortcuts import render
from .forms import CustomUserCreationForm

# 사용자 가입 처리
# GET: 사용자 가입 폼을 보여준다. (templates/account/create.html)
# POST: 사용자 가입 폼에서 입력한 값을 처리한다. (home으로 redirect)
def create(request):
    if request.method == "GET":
        # 사용자 가입 폼을 보여준다.
        return render(request, "account/create.html", {"form": CustomUserCreationForm()})
    else:
        # 사용자 가입 폼에서 입력한 값을 처리한다.
        pass