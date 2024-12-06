from tempfile import template

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm

from django.templatetags.static import static
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

from .forms import LoginForm
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm





urlpatterns = [
    path('', views.home),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<slug:val>', views.CategoryView.as_view(),name='category'),
    path('category-title/<val>', views.CategoryTitle.as_view(), name='category-title'),
    path('product-detail/<int:pk>', views.ProductDetail.as_view(), name='product-detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name='updateAddress'),
    path('add-to-cart/',views.add_to_cart, name="add_to_cart"),
    path('cart/', views.show_cart, name='showcart'),
path('checkout/', views.show_cart, name='checkout'),
path("callback/", views.mpesa_callback, name="mpesa_callback"),
# path('update-cart-quantity/', views.update_cart_quantity, name='update_cart_quantity'),
path('update-cart/', views.update_cart, name='update-cart'),
path('remove-cart/', views.remove_cart, name='remove-cart'),
path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/title/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/title/', views.remove_from_wishlist, name='remove_from_wishlist'),
    #login authentication
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='password_reset.html', form_class=MyPasswordResetForm),name='password_reset'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='changepassword.html',
    form_class=PasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),
    name='passwordchangedone'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
                name='password_reset_done'),
path('password-reset-confirm/<uidb64>/<token>',auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=MySetPasswordForm),
                name='password_reset_confirm'),
path('password-reset-complete',auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
                name='password_reset_done'),

              ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

