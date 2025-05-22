from typing import List, Optional, cast, Iterable
from django.db.models.query import QuerySet

import factory
from factory.faker import Faker

from common.models import Car, Component, ComponentRegionInfo, DUser, Region
from django.db.models.signals import post_save, pre_save
from common.tests.utils import generate_identifier


class RegionFactory(factory.django.DjangoModelFactory[Region]):
    class Meta:
        model = Region

    name = Faker("city")


class DUserFactory(factory.django.DjangoModelFactory[DUser]):
    class Meta:
        model = DUser

    username = Faker("user_name")
    email = Faker("email")


class CarFactory(factory.django.DjangoModelFactory[Car]):
    class Meta:
        model = Car

    code = Faker("ean8")

    @factory.post_generation
    def regions(
        self,
        create,
        extracted: Optional[Iterable[Region]] = None,
        **kwargs,
    ) -> None:
        if not create:
            return

        if not extracted:
            region_iterator: List["Region"] = RegionFactory.create_batch(
                kwargs.get("num_regions", 3)
            )
        else:
            region_iterator = cast(List["Region"], extracted)

        for region in region_iterator:
            self.regions.add(region)

    @factory.post_generation
    def components(self, create, extracted: int, **kwargs):
        if not create:
            return
        
        if not extracted or not isinstance(extracted, int):
            raise ValueError("You must provide a number of components to create.")
        elif extracted < 0:
            raise ValueError("The number of components must be a positive integer.")

        ComponentFactory.create_batch(extracted, car=self)


@factory.django.mute_signals(post_save, pre_save)
class ComponentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Component

    car = factory.SubFactory(CarFactory)

    name = Faker("word")
    owner = factory.SubFactory(DUserFactory)
    description = Faker("text")
    identifier = factory.Sequence(lambda n: generate_identifier(n))
    price = Faker("random_number", digits=5)
    weight = Faker("random_number", digits=3)
    quantity = Faker("random_number", digits=2)
    is_active = Faker("boolean")
    metadata = factory.LazyAttribute(lambda o: {"key": o.name})

    @factory.post_generation
    def region_info(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing
            return
        
        related_car = cast(Car, self.car)
        regions = cast(QuerySet[Region], related_car.regions.all())        
        for region in regions:
            ComponentRegionInfoFactory.create(
                tool=self,
                region=region,  # Override the region with the one created above
            )


@factory.django.mute_signals(post_save, pre_save)
class ComponentRegionInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ComponentRegionInfo

    region = factory.SubFactory(RegionFactory)
    tool = factory.SubFactory(ComponentFactory)
