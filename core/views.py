from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import Blog, Comment, Tutorial, Category, MentorshipChat, MentorshipMessage, User, Profile
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q, Count


from django.db.models import Q
from .models import MentorshipMessage

def custom_login_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You need to log in to access this page or perform this action.")
            return redirect(f"/?next={request.path}")
        return view_func(request, *args, **kwargs)
    return wrapped_view

def get_total_unread_messages(user):
    print(user)
    return MentorshipMessage.objects.filter(
        Q(chat__participant_one=user) | Q(chat__participant_two=user),
        is_read=False
    ).exclude(sender=user).count()

def landing_page(request):
    if request.user.is_authenticated:
        return redirect("core:posts")

    # Display a message if the user needs to log in
    if request.method == "POST":
        form_type = request.POST.get("form_type")
        
        # Handle sign-up form submission
        if form_type == "sign_up":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Account created successfully! You are now logged in.")
                return redirect("core:posts")
            else:
                messages.error(request, "Please correct the errors below.")

        # Handle sign-in form submission
        elif form_type == "sign_in":
            username_or_email = request.POST.get("usernameOrEmail")
            password = request.POST.get("password")
            user = authenticate(request, username=username_or_email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in!")
                return redirect("core:posts")
            else:
                messages.error(request, "Invalid username or password. Please try again.")

    form = CustomUserCreationForm()
    return render(request, "core/landing.html", {"form": form})


def posts_page(request):
    blogs = Blog.objects.all()[:2]
    trending_blogs = Blog.objects.annotate(
        popularity=Count('likes_dislikes') + Count('comments')
    ).order_by('-popularity')[:5] 
    
    total_unread_messages = None
    if request.user.is_authenticated:
        total_unread_messages = get_total_unread_messages(request.user)
    
    context = {
        'blogs': blogs,
        'trending_blogs': trending_blogs,
        'total_unread_messages': total_unread_messages  
    }
    return render(request, "core/posts.html", context)

def post_detail(request, post_id):
    total_unread_messages = None
    if request.user.is_authenticated:
        total_unread_messages = get_total_unread_messages(request.user)
    blog = get_object_or_404(Blog, id=post_id)
    comments_list = Comment.objects.filter(blog=blog).order_by('created_at')
    paginator = Paginator(comments_list, 5) 
    page_number = request.GET.get('page') 
    comments = paginator.get_page(page_number)  

    return render(request, 'core/post_detail.html', {'blog': blog, 'comments': comments, 'total_unread_messages': total_unread_messages})

@custom_login_required
def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            Comment.objects.create(user=request.user, content=content, blog=blog) 
            messages.success(request, "Your comment has been added.") 
        else:
            messages.error(request, "Comment cannot be empty.")

    return redirect('core:post_detail', post_id=blog_id)


def tutorials(request):
    total_unread_messages = None
    if request.user.is_authenticated:
        total_unread_messages = get_total_unread_messages(request.user)
    tutorials = Tutorial.objects.all()
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        tutorials = tutorials.filter(category__id=category_id)
    return render(request, 'core/tutorials.html', {
        'tutorials': tutorials,
        'categories': categories,
        'total_unread_messages': total_unread_messages
    })

def tutorial_detail(request, tutorial_id):
    total_unread_messages = None
    if request.user.is_authenticated:
        total_unread_messages = get_total_unread_messages(request.user)
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    comments_list = Comment.objects.filter(tutorial=tutorial).order_by('created_at')
    paginator = Paginator(comments_list, 5)
    page_number = request.GET.get('page') 
    comments = paginator.get_page(page_number) 
    return render(request, 'core/tutorial_detail.html', {
        'tutorial': tutorial,
        'comments': comments,
        'total_unread_messages': total_unread_messages 
    })

@custom_login_required
def add_tutorial_comment(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)

    if request.method == 'POST':
        content = request.POST.get('content')  

        if content:
            Comment.objects.create(user=request.user, content=content, tutorial=tutorial) 
            messages.success(request, "Your comment has been added.")
        else:
            messages.error(request, "Comment cannot be empty.") 

    return redirect('core:tutorial_detail', tutorial_id=tutorial_id)

@custom_login_required
def mentorship(request):
    total_unread_messages = None
    if request.user.is_authenticated:
        total_unread_messages = get_total_unread_messages(request.user)
    mentors = User.objects.filter(is_staff=True)
    user_chats = MentorshipChat.objects.filter(
        Q(participant_one=request.user) | Q(participant_two=request.user)
    ).annotate(
        unread_count=Count(
            'messages', 
            filter=Q(messages__is_read=False) & ~Q(messages__sender=request.user)
        )
    ).order_by('-last_message_date')
    return render(request, 'core/mentorship.html', {
        'mentors': mentors,
        'chats': user_chats,
        'total_unread_messages': total_unread_messages
    })

@custom_login_required
def chat_detail(request, id, id_type):
    participant_one = request.user
    total_unread_messages = None
    if request.user.is_authenticated:
        total_unread_messages = get_total_unread_messages(request.user)
    if id_type == 'chat_id':
        chat = get_object_or_404(MentorshipChat, id=id)
        messages = MentorshipMessage.objects.filter(chat=chat).order_by('created_at')
        participant_two = chat.participant_two
        created = False
        
    elif id_type == 'recipient_id':
        chat, created = MentorshipChat.objects.get_or_create(
            participant_one=participant_one,
            participant_two_id=id,
            defaults={'created_at': timezone.now()}
        )
        messages = MentorshipMessage.objects.filter(chat=chat).order_by('created_at')
        participant_two = get_object_or_404(User, id=id)
        
    else:
        print("id type", id_type)
        return render(request, 'core/error.html', {'message': 'Invalid ID type specified.'})
    
    if created:
        print("A new chat was created.")

    # Update unread messages
    unread_messages = messages.exclude(sender=request.user).filter(is_read=False)
    unread_messages.update(is_read=True)
    
    context = {
        'chat': chat,
        'messages': messages,
        'chat_created': created,
        'user': participant_one,
        'participant_two': participant_two,
        'total_unread_messages': total_unread_messages,
    }
    
    return render(request, 'core/chat_detail.html', context)


@custom_login_required
def send_message(request, chat_id):
    chat = get_object_or_404(MentorshipChat, id=chat_id)
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            print(chat)
            MentorshipMessage.objects.create(
                chat=chat,
                sender=request.user,
                content=message_text,
                created_at=timezone.now()
            )
            chat.last_message = message_text
            chat.last_message_date = timezone.now()
            chat.save()
            id_type = 'chat_id'  
            
            return redirect('core:chat_detail', id=chat_id, id_type='chat_id')

    return redirect('core:chat_detail', id=chat_id, id_type='chat_id')


def profiles(request):
    journalist_profiles = Profile.objects.all()
    return render(request, 'core/profiles.html', {'journalist_profiles': journalist_profiles})

def journalist_detail_view(request, id):
    # Fetch the journalist profile based on the ID
    profile = get_object_or_404(Profile, id=id)
    
    # Render the template with the profile context
    return render(request, 'core/journalist_detail.html', {'profile': profile})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('core:posts')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'core/landing.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('core:landing')
