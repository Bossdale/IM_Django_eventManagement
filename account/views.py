from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib import messages


class LoginView(View):
    # Make sure this matches your actual template location
    template_name = 'account/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # 1. Get the data from the HTML form names
        username_data = request.POST.get('username')
        password_data = request.POST.get('password')

        # 2. Check credentials against Django's database
        user = authenticate(request, username=username_data, password=password_data)

        if user is not None:
            # 3. If correct, log them in
            login(request, user)

            # Redirect to your home page (CreateEvent index)
            return redirect('CreateEvent:index')
        else:
            # 4. If wrong, reload the page with an error message
            messages.error(request, "Invalid username or password")
            return render(request, self.template_name)