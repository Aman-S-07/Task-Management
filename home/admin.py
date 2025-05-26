from django.contrib import admin
from .models import Category, Contact, Task

admin.site.register(Task)




try:
    @admin.register(Task)
    class TaskAdmin(admin.ModelAdmin):
        list_display = ('name', 'category', 'start_date', 'end_date', 'priority', 'location', 'organizer', 'assigned_to')
        list_filter = ('category', 'priority')
        search_fields = ('name', 'category__name', 'description', 'location', 'organizer')
except admin.sites.AlreadyRegistered:
    print("Task model is already registered")

try:
    @admin.register(Category)
    class CategoryAdmin(admin.ModelAdmin):
        list_display = ('name',)
        search_fields = ('name',)
except admin.sites.AlreadyRegistered:
    print("Category model is already registered")
    
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'date')
    search_fields = ('name', 'email')
    


from home.models import Intern

@admin.register(Intern)
class InternAdmin(admin.ModelAdmin):
    list_display = ('user',)




