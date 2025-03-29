from django.views import View
from django.shortcuts import redirect, render


class RedirectToHomeView(View):
    """
    View que redireciona para a rota 'home' quando acessada.
    Você pode ajustar o destino alterando o argumento passado para a função redirect.
    """

    def get(self, request, *args, **kwargs):
        return redirect('login')


class HelloView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "app/hello.html")
