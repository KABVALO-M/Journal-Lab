from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Blog, Tutorial, Category, Profile, Certificate, Skill, Achievement, WorkExperience, User

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

# Register the User model with the custom UserAdmin
admin.site.register(User, UserAdmin)

class BlogAdmin(admin.ModelAdmin):
    # Display the following fields in the list view
    list_display = ('title', 'author', 'created_at', 'updated_at')
    
    # Enable filtering by author and created date
    list_filter = ('author', 'created_at')
    
    # Enable searching by title and content
    search_fields = ('title', 'content')
    
    # Customize form layout and fields in the admin form
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author', 'image', 'video')
        }),
    )

    # Set the author field to default to the currently logged-in user
    def save_model(self, request, obj, form, change):
        if not change:  # Only set author when creating a new blog post
            obj.author = request.user
        super().save_model(request, obj, form, change)

# Register the Blog model with the custom admin class
admin.site.register(Blog, BlogAdmin)


# Create admin class for Tutorial
class TutorialAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'category')  # Fields to display
    search_fields = ('title', 'content')  # Fields to search in admin
    list_filter = ('created_at', 'author', 'category')  # Fields to filter by
    ordering = ('-created_at',)  # Default ordering

# Create admin class for Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')  # Fields to display
    search_fields = ('name',)  # Fields to search in admin
    ordering = ('-created_at',)  # Default ordering

# Register the models with the admin site
admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(Category, CategoryAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'contact_number')
    search_fields = ('user__username', 'location')
    list_filter = ('location',)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'institution', 'date_issued')
    search_fields = ('title', 'institution')
    list_filter = ('date_issued',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name')
    search_fields = ('name',)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'date_achieved')
    search_fields = ('title',)
    list_filter = ('date_achieved',)

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'job_title', 'company_name', 'start_date', 'end_date')
    search_fields = ('job_title', 'company_name')
    list_filter = ('start_date', 'end_date', 'profile')