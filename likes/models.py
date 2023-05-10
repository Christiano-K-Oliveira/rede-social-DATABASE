from django.db import models


# Create your models here.
class Like(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    user_like = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="users_like")
    publication = models.ForeignKey("publications.Publication", on_delete=models.CASCADE, related_name="publication_like")

    def __str__(self) -> str:
        return f'<UserLike: {self.user_like} - Publication: {self.publication}>'
