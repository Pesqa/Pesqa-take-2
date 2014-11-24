from django.test import TestCase
from django.db.utils import IntegrityError

from trip.models import FishType, TripImage, MasterTrip, TripInstance, TripBooking

class FishTypeTest(TestCase):
    
    def test_saving_and_retrieving_fishtypes(self):
        type1 = FishType()
        type1.name = "Testing"
        type1.save()
        
        saved_fish_type = FishType.objects.all()
        self.assertEqual(saved_fish_type.count(), 1)
    
    def test_fishtype_must_by_unique(self):
        type1 = FishType()
        type1.name = "Fishtype 1"
        type1.save()
        
        type2 = FishType()
        type2.name = "Fishtype 1"
        self.assertRaises(IntegrityError, type2.save)

    def test_fishtype_alphabetical_order(self):
        type1 = FishType()
        type1.name = "A"
        type1.save()
        
        type2 = FishType()
        type2.name = "C"
        type2.save()
        
        type3 = FishType()
        type3.name = "E"
        type3.save()
        
        type4 = FishType()
        type4.name = "B"
        type4.save()
        
        type5 = FishType()
        type5.name = "D"
        type5.save()
        
        types = list(FishType.objects.values_list('name', flat=True))
        self.assertListEqual(["A","B","C","D","E"], types)
        