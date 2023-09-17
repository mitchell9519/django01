'''Defines url patterns for app'''


from django.urls import path

from . import views

app_name ='learning_logs'

urlpatterns = [
    #homepage
    path('', views.index, name='index'),
    #page, shows all topics
    path('topics/',views.topics,name='topics'),
    #detail dfor single topic
    path('topics/<int:topic_id>/',views.topic,name='topic'),
    #adding new topic
    path('new_topic/',views.new_topic, name='new_topic'),
    #adding new entry
    path('new_entry/<int:topic_id>/',views.new_entry, name='new_entry'),
    #Edit_entry
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]