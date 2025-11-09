from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.NewQuestionsView.as_view(), name='new_questions'),

    path('hot/', views.HotQuestionsView.as_view(), name='hot_questions'),

    path('tag/<str:tag_name>/', views.QuestionsByTagView.as_view(), name='questions_by_tag'),

    path('question/<int:question_id>/', views.QuestionDetailView.as_view(), name='question_detail'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('ask/', views.AskQuestionView.as_view(), name='ask'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
]