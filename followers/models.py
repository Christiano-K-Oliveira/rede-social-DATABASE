from django.db import models


# Create your models here.
class Follower(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    user_follower = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="users_follower")
    user_following = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="users_following")

    def __str__(self) -> str:
        return f'<Follower {self.user_follower} - Following: {self.user_following}>'
