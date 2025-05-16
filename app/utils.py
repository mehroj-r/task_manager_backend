from django.contrib.auth.models import BaseUserManager

class TelegramUserManager(BaseUserManager):
    def create_user(self, id, **extra_fields):
        if not id:
            raise ValueError("The Telegram ID must be set")
        user = self.model(
            id=id,
            **extra_fields
        )
        # no password for bot users
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, id, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        if not id:
            raise ValueError("The Telegram ID must be set")
        user = self.model(
            id=id,
            **extra_fields
        )

        # Superusers get proper password
        user.set_password(extra_fields.get("password"))
        user.save(using=self._db)
        return user