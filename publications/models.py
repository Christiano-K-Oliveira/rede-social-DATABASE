from django.db import models


# Create your models here.
class PermissionsFields(models.TextChoices):
    PUBLIC = "public"
    PRIVATE = "private"


class Publication(models.Model):
    title = models.CharField(max_length=80)
    text = models.TextField(max_length=2000)
    permission = models.CharField(
        max_length=20,
        choices=PermissionsFields.choices,
        default=PermissionsFields.PUBLIC
    )
    photo_url = models.CharField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user_publication = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="user_publications")

    def __str__(self) -> str:
        return f'<UserPublication: {self.user_publication} - Title: {self.title} - Permission: {self.permission}>'
