from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')  # Replace with your desired redirect URL
@login_required
def view_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('home')  # Replace with your desired redirect URL
    return render(request, 'profile.html', {'user': user})      