from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    career_journey = models.TextField(blank=True, help_text="A brief overview of the career journey.")
    location = models.CharField(max_length=255, blank=True, help_text="User's current location.")
    contact_number = models.CharField(max_length=15, blank=True, help_text="Contact phone number.")

    twitter = models.URLField(blank=True, help_text="URL to Twitter profile.")
    linkedin = models.URLField(blank=True, help_text="URL to LinkedIn profile.")
    facebook = models.URLField(blank=True, help_text="URL to Facebook profile.")
    instagram = models.URLField(blank=True, help_text="URL to Instagram profile.")

    def __str__(self):
        return f"{self.user.username}'s Profile"
    

class Certificate(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='certificates')
    title = models.CharField(max_length=255, help_text="Title of the certificate.")
    institution = models.CharField(max_length=255, help_text="Institution that issued the certificate.")
    date_issued = models.DateField(help_text="Date the certificate was issued.")
    description = models.TextField(blank=True, help_text="Optional description of the certificate.")

    def __str__(self):
        return f"{self.title} from {self.institution}"

class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100, help_text="Name of the skill.")

    def __str__(self):
        return self.name

class Achievement(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=255, help_text="Title of the achievement.")
    date_achieved = models.DateField(help_text="Date when the achievement was obtained.")
    description = models.TextField(blank=True, help_text="Description of the achievement.")

    def __str__(self):
        return self.title

class WorkExperience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='work_experience')
    job_title = models.CharField(max_length=255, help_text="Job title.")
    company_name = models.CharField(max_length=255, help_text="Name of the company.")
    start_date = models.DateField(help_text="Start date of employment.")
    end_date = models.DateField(null=True, blank=True, help_text="End date of employment (leave blank if current).")
    responsibilities = models.TextField(blank=True, help_text="Responsibilities in this role.")

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Tutorial Model
class Tutorial(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video = models.FileField(upload_to='tutorial_videos/', null=True, blank=True)  # Field for video
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tutorials', default=1)

    def __str__(self):
        return self.title


# Blog Model
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Media fields, allowing either image or video but not both
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    video = models.FileField(upload_to='blog_videos/', blank=True, null=True)

    def clean(self):
        # Ensure only one media file (image or video) is uploaded
        if self.image and self.video:
            raise ValidationError("Only one media type can be uploaded: either an image or a video, not both.")

    def save(self, *args, **kwargs):
        # Run the custom validation before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# Comment Model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")

    def __str__(self):
        return f"Comment by {self.user.username} on {'Tutorial' if self.tutorial else 'Blog'}"


# LikeDislike Model
class LikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, null=True, blank=True, related_name="likes_dislikes")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True, related_name="likes_dislikes")
    is_like = models.BooleanField(default=True)  # True for like, False for dislike

    class Meta:
        unique_together = (("user", "tutorial"), ("user", "blog"))

    def __str__(self):
        item = self.tutorial or self.blog
        item_type = 'Tutorial' if self.tutorial else 'Blog'
        return f"{'Like' if self.is_like else 'Dislike'} by {self.user.username} on {item_type}: {item}"


class MentorshipChat(models.Model):
    participant_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_chats')
    participant_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    last_message = models.TextField(blank=True, null=True)  # To store the last message
    last_message_date = models.DateTimeField(auto_now=True)  # To store the date of the last message

    def __str__(self):
        return f'Chat between {self.participant_one} and {self.participant_two}'
    def get_unread_messages(self): return self.messages.filter(is_read=False, sender__ne=self)
    



class MentorshipMessage(models.Model):
    chat = models.ForeignKey(MentorshipChat, null=True, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Track if the message has been read

    def __str__(self):
        return f"Message from {self.sender.username} in chat {self.chat.id} at {self.created_at}"


