from django.db import models


# Create your models here.
class StatusFields(models.TextChoices):
    ACCEPTED = "Accepted"
    REFUSED = "Refused"
    REQUESTED = "Requested"


class Friendship(models.Model):
    status = models.CharField(
        choices=StatusFields.choices,
        max_length=20
    )
    created_at = models.DateTimeField(auto_now_add=True)

    user_request = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="users_request")
    user_friendship = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="users_friendhip")

    def __str__(self) -> str:
        return f'<UserRequest: {self.user_request} - UserFriendship: {self.user_friendship} - Status: {self.status}>'
