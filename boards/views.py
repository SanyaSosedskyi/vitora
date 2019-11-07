from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm, BoardCreateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.db.models import Count
from accounts.models import User
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.messages import get_messages


def home(request):
    board_list = Board.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(board_list, 5)
    try:
        boards = paginator.page(page)
    except PageNotAnInteger:
        boards = paginator.page(1)
    except EmptyPage:
        boards = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'boards': boards, 'page': page})


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        session_key = f'viewed_topic_{self.topic.pk}'
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=board.pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_at = timezone.now()
        post.updated_by = self.request.user
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your account was updated successfully!')
        return redirect('my_account')

    def form_invalid(self, form):
        messages.warning(self.request, 'Please correct the error below')
        return redirect('my_account')

    def get_object(self):
        return self.request.user


@login_required
def save_board_form(request, form, template_name, messagess, page):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            board_list = Board.objects.all()
            paginator = Paginator(board_list, 5)
            try:
                boards = paginator.page(page)
            except PageNotAnInteger:
                boards = paginator.page(1)
            except EmptyPage:
                boards = paginator.page(paginator.num_pages)
            data['contentBlock'] = render_to_string('home.html', {
                'boards': boards,
                'user': request.user,
                'messages': messagess,
                'page': page
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form, 'page': page}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def board_create(request, page):
    if request.method == "POST":
        form = BoardCreateForm(request.POST)
        messages.success(request, 'The board has been created!')
        messagess = get_messages(request)
    else:
        form = BoardCreateForm()
        messagess = None

    return save_board_form(request, form, 'includes/partial_board_create.html', messagess, page)


@login_required
def board_update(request, pk, page):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = BoardCreateForm(request.POST, instance=board)
        messages.success(request, 'The board has been created!')
        messagess = get_messages(request)
    else:
        form = BoardCreateForm(instance=board)
        messagess = None
    return save_board_form(request, form, 'includes/partial_board_update.html', messagess, page)


@login_required
def board_delete(request, pk, page):
    board = get_object_or_404(Board, pk=pk)
    data = dict()
    if request.method == 'POST':
        board.delete()
        data['form_is_valid'] = True
        board_list = Board.objects.all()
        paginator = Paginator(board_list, 5)
        try:
            boards = paginator.get_page(page)
        except PageNotAnInteger:
            boards = paginator.get_page(1)
        except EmptyPage:
            boards = paginator.page(paginator.num_pages)
        messages.success(request, 'The board has been deleted!')
        messagess = get_messages(request)
        data['contentBlock'] = render_to_string('home.html', {
            'boards': boards,
            'user': request.user,
            'messages': messagess,
            'page': page
        })
    else:
        context = {'board': board, 'page': page}
        data['html_form'] = render_to_string('includes/partial_board_delete.html', context=context, request=request)
    return JsonResponse(data)



