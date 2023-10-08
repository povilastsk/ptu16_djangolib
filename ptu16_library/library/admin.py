from django.contrib import admin
from . import models


class BoookInstanceInline(admin.TabularInline):
    model = models.BookInstance
    readonly_fields = ("unique_id", )
    can_delete = False
    extra = 0


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "display_genre")
    inlines = [BoookInstanceInline]
    search_fields = ("title", "summary", "author__last_name")


@admin.register(models.BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("unique_id", "book", "reader", "status", "due_back")
    list_filter = ('status', "due_back")
    readonly_fields = ("unique_id", )
    search_fields = ("unique_id", "book__title", "book__author__last_name", "reader__last_name", "reader__user_name")
    fieldsets = (
        ("Identification", {"fields": (("book", "unique_id"),)}),
        ("Availability", {"fields": (("status", "reader", "due_back"),)}),
    )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "display_books")
    list_display_links = ("last_name", "first_name")


@admin.register(models.BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'reviewer', 'created_at')
    list_display_links = ('created_at', )
    

admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Genre)
# admin.site.register(models.Bookinstance , BookInstanceAdmin)