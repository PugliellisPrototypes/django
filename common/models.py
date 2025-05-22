from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class DUser(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


class Car(models.Model):
    code = models.CharField(max_length=10, unique=True)
    regions = models.ManyToManyField(Region, related_name="cars")


class Component(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="components")

    name = models.CharField(max_length=100)
    description = models.TextField()
    identifier = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(DUser, on_delete=models.CASCADE, related_name="tools")
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.FloatField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class ComponentRegionInfo(models.Model):
    component = models.ForeignKey(
        Component, on_delete=models.CASCADE, related_name="region_info"
    )
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    # Additional fields for the relationship
    info = models.CharField(max_length=255)
    creation_target = models.DateField(null=True, blank=True)
    availability = models.BooleanField(default=True)
    stock_level = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.component.name} - {self.region.name}"
