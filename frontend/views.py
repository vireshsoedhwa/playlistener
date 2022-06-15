from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.

@ensure_csrf_cookie
def index(request):

    if request.session.test_cookie_worked():
        print(str(request.headers['Cookie']))

    request.session.set_test_cookie()

    context = {
        'version': '',
    }

    return render(request, 'frontend/index.html', context)
