from django.test import TestCase
from common.tests.factories import (
    RegionFactory,
    DUserFactory,
    CarFactory,
    ComponentFactory,
    ComponentRegionInfoFactory,
)
from common.models import Region, DUser, Car, Component, ComponentRegionInfo
from typing import Iterable, Optional, List, Any

class ExampleTestCase(TestCase):
    regions: List[Region]
    users: List[DUser]
    car: Car  

    @classmethod
    def setUpTestData(cls) -> None:
        cls.regions = RegionFactory.create_batch(4)
        cls.users = DUserFactory.create_batch(3)

        cls.car = CarFactory.create(
            regions=cls.regions,
            components=20,  
        )
        print(cls.car)

    def test_example(self) -> None:
        self.assertEqual(self.car.regions.count(), 4)
