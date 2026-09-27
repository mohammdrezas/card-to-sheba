from django.db import models
import uuid

class Inquiry(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"
        TIMEOUT = "TIMEOUT", "Timeout"
        REJECTED = "REJECTED", "Rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    masked_card_number = models.CharField(max_length=16)
    card_fingerprint = models.CharField(max_length=64)
    sheba = models.CharField(max_length=36, null=True, blank=True)
    error_code = models.CharField(max_length=50, null=True, blank=True)
    external_http_status = models.IntegerField(null=True, blank=True)
    external_reference_id = models.CharField(max_length=64, null=True, blank=True)
    processing_duration_ms = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["card_fingerprint"]),
        ]

    def __str__(self):
        return f"{self.id} - {self.status}"