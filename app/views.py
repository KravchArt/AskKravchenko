from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


# пагинация
def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page


# Базовый класс
class BaseQuestionView(TemplateView):
    template_name = 'index.html'

    def get_questions_data(self):
        """Рыба вопросов"""
        questions = []
        for i in range(1, 50):
            questions.append({
                'title': f'Вопрос заголовок {i}',
                'id': i,
                'text': f'Это текст вопроса {i}. Бла бла бла бла бла, тут что-то сос мыслом',
                'tags': ['django', 'python', 'vk_education'],
                'answers': i * 2,
                'votes': i,
                'user': f'user{i}',
                'views': i * 7
            })
        return questions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = self.get_questions_data()
        context['page_obj'] = paginate(questions, self.request, 10)
        context['questions'] = questions
        return context


# Главная страница
class NewQuestionsView(BaseQuestionView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Новые вопросы'
        return context


# Порулярные вопросы
class HotQuestionsView(BaseQuestionView):
    def get_questions_data(self):
        questions = []
        for i in range(1, 50):
            questions.append({
                'title': f'Популярный вопрос {i}',
                'id': i,
                'text': f'Это популярный вопрос {i} с большим количеством голосов и ответов.',
                'tags': ['popular', 'hot', 'trending'],
                'answers': i * 3,
                'votes': i + 20,
                'user': f'user{i}',
                'views': i * 15
            })
        return questions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Популярные вопросы'
        return context


# Вопросы по тегу
class QuestionsByTagView(BaseQuestionView):
    def get_questions_data(self):
        tag_name = self.kwargs.get('tag_name')
        questions = []
        for i in range(1, 20):
            questions.append({
                'title': f'Вопрос с тегом {tag_name} {i}',
                'id': i,
                'text': f'Этот вопрос имеет тег {tag_name}. Бла бла бла, сос мыслом',
                'tags': [tag_name, 'other'],
                'answers': i,
                'votes': i,
                'user': f'user{i}',
                'views': i * 3
            })
        return questions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_name'] = self.kwargs.get('tag_name')
        return context


class QuestionDetailView(TemplateView):
    template_name = 'question.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        question_id = self.kwargs.get('question_id')
        context['question'] = {
            'id': question_id,
            'title': f'Вопрос {question_id}',
            'text': f'Подробный текст для вопроса {question_id}. Это более длинное описание проблемы, которая требует решения. Здесь может быть код, ошибки и дополнительная информация.',
            'tags': ['django', 'python', 'web'],
            'votes': 15,
            'user': 'asker_user'
        }

        # Генерируем ответы
        answers = []
        for i in range(1, 15):
            answers.append({
                'id': i,
                'text': f'Это ответ {i} для вопроса {question_id}. Здесь содержится решение проблемы или полезная информация по вопросу.',
                'votes': i - 3,
                'user': f'answer_user{i}',
                'is_correct': i % 3 == 0
            })

        # Добавляем пагинированные ответы
        context['page_obj'] = paginate(answers, self.request, 5)
        return context


class AskQuestionView(LoginRequiredMixin, TemplateView):
    template_name = 'ask.html'
    login_url = '/login/'


class LoginView(TemplateView):
    template_name = 'login.html'


class SignupView(TemplateView):
    template_name = 'signup.html'


class ProfileEditView(LoginRequiredMixin, TemplateView):
    template_name = 'signup.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        context['user'] = self.request.user
        return context