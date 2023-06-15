"""
URL configuration for expmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from expenses import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'expense'

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.index, name='index'),
    path("tasks/", views.tasks, name='tasks'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),


    # Event detail
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),

    # Expense
    path('event/<int:event_id>/expense/create/',
         views.create_expense, name='create_expense'),
    path('expense/<int:expense_id>/update/',
         views.update_expense, name='update_expense'),
    path('expense/<int:expense_id>/delete/',
         views.delete_expense, name='delete_expense'),

    # Task
    path('newtask',
         views.create_task, name='newtask'),
    path('task/<int:task_id>/update/', views.update_task, name='update_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('dashboard/', views.dashboard, name="dashboard")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
