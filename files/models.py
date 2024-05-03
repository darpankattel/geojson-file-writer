from django.db import models
import os

# Create your models here.


class GeoJsonFile(models.Model):
    """
    An instance of a GeoJson file
    """
    FILE_TYPES = (
        ("FeatureCollection", "FeatureCollection"),
        ("Feature", "Feature"),
    )
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, help_text="Title of the file")
    description = models.TextField(
        null=True, blank=True, help_text="Description of the file | Optional")
    created_at = models.DateTimeField(auto_now_add=True)

    type_of_file = models.CharField(max_length=255, choices=FILE_TYPES, default="FeatureCollection",
                                    help_text="Type of the file")

    completed = models.BooleanField(
        default=False, help_text="Is the file completed?")
    output = models.FileField(upload_to="geojson", null=True, blank=True)

    def __str__(self):
        return self.title

    def random_name(self):
        return str(self.id)

    def get_filepath(self):
        # import media path
        from django.conf import settings

        return os.path.join(settings.MEDIA_ROOT, "geojson", self.random_name())

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "GeoJson File"
        verbose_name_plural = "GeoJson Files"


class Chunk(models.Model):
    """
    A chunk of a GeoJson file
    """

    id = models.BigAutoField(primary_key=True)
    json = models.JSONField()
    file = models.ForeignKey(GeoJsonFile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File {self.file.title} | Chunk {self.id}"

    class Meta:
        ordering = ["file", "-created_at"]
        verbose_name = "GeoJson Chunk"
        verbose_name_plural = "GeoJson Chunks"
