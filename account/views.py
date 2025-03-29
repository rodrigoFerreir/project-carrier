from django.contrib.auth import login as auth_login
from django.contrib.auth.views import (
    LoginView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render


from .forms import CustomUserForm, MyAuthenticationForm
from .models import User


def signup(request):
    '''
    Cadastra Usuário.
    '''
    template_name = 'registration/registration_form.html'
    form = CustomUserForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, template_name)


class MyPasswordResetConfirm(PasswordResetConfirmView):
    '''
    Requer password_reset_confirm.html
    '''

    def form_valid(self, form):
        self.user.is_active = True
        self.user.save()
        return super(MyPasswordResetConfirm, self).form_valid(form)


class MyPasswordResetComplete(PasswordResetCompleteView):
    '''
    Requer password_reset_complete.html
    '''

    ...


class MyPasswordReset(PasswordResetView):
    '''
    Requer
    registration/password_reset_form.html
    registration/password_reset_email.html
    registration/password_reset_subject.txt  Opcional
    '''

    ...


class MyPasswordResetDone(PasswordResetDoneView):
    '''
    Requer
    registration/password_reset_done.html
    '''

    ...


def user_list(request):
    template_name = 'accounts/user_list.html'
    object_list = User.objects.exclude(email='admin@email.com')
    context = {'object_list': object_list}
    return render(request, template_name, context)


def user_detail(request, pk):
    template_name = 'accounts/user_detail.html'
    instance = get_object_or_404(User, pk=pk)

    context = {'object': instance}
    return render(request, template_name, context)


def user_create(request):
    template_name = 'accounts/user_form.html'
    form = CustomUserForm(request.POST or None)

    context = {'form': form}
    return render(request, template_name, context)


def user_update(request, pk):
    template_name = 'accounts/user_form.html'
    instance = get_object_or_404(User, pk=pk)
    form = CustomUserForm(request.POST or None, instance=instance)

    context = {
        'object': instance,
        'form': form,
    }
    return render(request, template_name, context)


class MyLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = MyAuthenticationForm

    def form_invalid(self, form):
        email = form.data.get('username')

        if email:
            try:
                user = User.objects.get(email=email)

                for error in form.errors.as_data()['__all__']:
                    if error.code == 'max_attempt':
                        # Envia email para o usuário resetar a senha.
                        print("Deveria resetar a senha")

            except User.DoesNotExist:
                pass
            else:
                # Dispara o signal quando o usuário existe, mas a senha está errada.
                print("Deveria avisar que o usuario esta con a senha errada")

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        redirect_to = "/app/veiculos/"
        user = form.get_user()

        # Autentica usuário
        auth_login(self.request, user)

        return HttpResponseRedirect(redirect_to)
