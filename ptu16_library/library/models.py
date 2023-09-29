from django.db import models
from django.utils.translation import gettext_lazy as _ 
from django.urls import reverse
import uuid

# Create your models here.

class Genre(models.Model):

    name= models.CharField((""), max_length=50, db_index=True)

    class Meta:
        verbose_name = _("genre")
        verbose_name_plural = _("grenres")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("genre_detail", kwargs={"pk": self.pk})

class Author(models.Model):
    first_name = models.CharField(_("first name"), max_length=100, db_index=True)
    last_name = models.CharField(_("last name"), max_length=100, db_index=True)

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse("Author_detail", kwargs={"pk": self.pk})

class Book(models.Model):
    title = models.CharField(_("title"), max_length=250, db_index=True)
    author = models.ForeignKey(
        Author,
        verbose_name=_("author"),
        on_delete=models.CASCADE,
        related_name="books",
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name=_("genres"),
        related_name="books",
    )
    summary = models.TextField(_("summary"))

    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("books")
        ordering = ["title"]

    def __str__(self):
        return f"{self.author} - {self.title}"

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})


LOAN_STATUS = (
    (0, _("available")),
    (1, _("reserved")),
    (2, _("taken")),
    (3, _("unavailable")),
)


class Bookinstance(models.Model):
    unique_id = models.UUIDField(_("unique ID"), db_index=True, unique=True)
    book = models.ForeignKey(
        Book, 
        verbose_name=_(""),
        on_delete=models.CASCADE,
        related_name="instances",
    )
    due_back = models.DateField(
        _("due back"), null=True, blank=True, db_index=True
    )
    status = models.PositiveSmallIntegerField(
        _("status"), choices=LOAN_STATUS, default=0
    )

    class Meta:
        verbose_name = _("book instance")
        verbose_name_plural = _("book instances")
        ordering = ["due_back"]

    def __str__(self):
        return f"{self.book} UUID: {self.unique_id}"

    def get_absolute_url(self):
        return reverse("bookinstance_detail", kwargs={"pk": self.pk})

