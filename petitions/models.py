from django.db import models  # Import Django models module for defining database model
from django.contrib.auth.models import User  # Import the built-in User model for relations


class Petition(models.Model):
    """A petition suggesting a movie be added to the catalog.

    Each field below has an inline comment describing its purpose.
    """
    id = models.AutoField(primary_key=True)  # Primary key for the petition
    title = models.CharField(max_length=255)  # Short title for the requested movie
    description = models.TextField(blank=True)  # Optional longer explanation
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petitions')  # User who created the petition
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when petition was created
    yes_votes = models.ManyToManyField(User, related_name='petition_yes_votes', blank=True)  # Users who voted YES
    no_votes = models.ManyToManyField(User, related_name='petition_no_votes', blank=True)  # Users who voted NO

    def yes_count(self):
        """Return the number of affirmative votes."""
        return self.yes_votes.count()  # Count yes_votes M2M

    def no_count(self):
        """Return the number of negative votes."""
        return self.no_votes.count()  # Count no_votes M2M

    def __str__(self):
        """Human-readable representation used in admin and shells."""
        return f"{self.id} - {self.title}"