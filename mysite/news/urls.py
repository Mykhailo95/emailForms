from django.urls import path
from .views import *


urlpatterns = [

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # send_email
    path('email/', form_email, name='email'),

    # path('testPaginate/',testPaginate, name='paginates'),# for function 
    path('', HomeNews.as_view(), name='home'),
    # path('', index, name='home'),
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
    # path('category/<int:category_id>/', get_category, name='category'),
    path('news/<int:news_id>/', ViewNews.as_view(), name='view_news'),
    # path('news/<int:news_id>/', view_news, name='view_news'),#для button Read more
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
    # path('news/add-news/', add_news, name='add_news'),#для button Read more
]