import pytz

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.functional import cached_property
from django.core.validators import MaxValueValidator
from django.template import Context

from utils.models import TimeStampedModel
from utils.helpers import file_url

class FishType(TimeStampedModel):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class TripImage(TimeStampedModel):
    image = models.ImageField(upload_to=file_url(u'trip_images'))

class MasterTrip(TimeStampedModel):
    name = models.CharField(max_length=150)
    fish_types = models.ManyToMany(FishType)
    fishing_type = models.CharField(max_length=50, choices=FISHING_TYPES)
    water_type = models.CharField(max_length=25, choices=WATER_TYPES)
    service_type = models.CharField(max_length=25, choices=SERVICE_TYPES)
    video_link = models.URLField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to=file_url(u'trip_images'))
    images = models.OneToMany(TripImage, blank=True, null=True)
    #provider = 
    featured = models.BooleanField(default=False)
    has_remaining = models.BooleanField(default=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pricing_model = models.CharField(max_length=50, choices=PRICING_TYPES)
    number_of_spots = models.CharField(max_length=50, choices=ANGLER_NUMS, blank=True, default="1")
    boat_group_size = models.PositiveIntegerField(validators=[MaxValueValidator(50)], default=1, blank=True)
    max_boat_group_size = models.PositiveIntegerField(validators=[MaxValueValidator(50)], default=0, blank=True)
    cost_per_extra_person = models.PositiveIntegerField(default=0, blank=True)
    
    description = models.TextField(default='', blank=True)
    description_location = models.TextField(default='', blank=True)
    description_fishing = models.TextField(default='', blank=True)
    description_accommondations = models.TextField(default='', blank=True)
    description_daily_program = models.TextField(default='', blank=True)
    description_food = models.TextField(default='', blank=True)
    description_travel = models.TextField(default='', blank=True)
    
    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return self.name
    
    @property
    def hero_image(self):
        return static('img/trip_hero/{}_hero_image.jpg'.format(self.service_type))
    
    @property
    def min_price(self):
        return self.upcoming_available_trips.aggregate(models.Min('price'))['price__min'] or self.price
    
    @property
    def has_any_remaining(self):
        return self.upcoming_available_trips.exists()
    
    def get_absolute_url(self):
        return reverse('master_detail', args=[self.pk])
    
    @cached_property
    def upcoming_available_trips(self):
        return self.instances.filter(begin__gt=datetime.now(pytz.utc), is_available=True)
    
    def number_of_instances(self):
        return self.upcoming_available_trips.count()
    
    def serialized_for_search(self):
        return {
            'link': self.get_absolute_url(),
            'img': self.thumbnail.url,
            'location': ', '.join([self.city, self.state]),
            'species': ', '.join(map(unicode, self.fish_types.all())),
            'price': str(floatformat(self.search_price, -2)),
            'name': self.name
            'description': self.description[:72] + '... '
        }
    

class TripInstance(TimeStampedModel):
    master_trip = models.ForeignKey(MasterTrip, related_name='instances')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_spots = models.PositiveIntegerField()
    begin = models.DateTimeField()
    end = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['begin']
    
    def __str__(self):
        # XXX -- DO NOT CHANGE WITHOUT CARE -- used in several places: e.g. provider_bookings
        return self.master_trip.name + ': {0.month}/{0.year} - {1.month}/{1.day}/{1.year}'.format(self.begin self.end)
    
    @property
    def spots(self):
        return self.number_of_spots - (self.booking_count or 0)

    @property
    def remaining_spots(self):
        return self.number_of_spots - self.total_bookings
    
    @property
    def total_bookings(self):
        return self.bookings.aggregate(models.Sum('num_booked'))['num_booked__sum'] or 0
    
class TripBooking(TimeStampedModel):
    trip = models.ForeignKey(TripInstance, related_name='bookings', null=True, on_delete=models.SET_NULL)
    #customer = models.ForeignKey(Customer)
    num_booked = models.PositiveIntegerField()
    amount_charged = models.DecimalField(max_digits=10, decimal_places=2)
    charged_id = models.CharField(max_length=60)
    
    def send_confirmation_email(self):
        context = Context({'booking': self})
        msg = render_to_string('booking_confirmation_email.txt', context)
        send_mail('Pesqa booking confirmation', msg, 'hello@pesqa.com', [self.customer.user.email])
        
    def __str__(self):
        return ': ' + str(self.num_booked) + 'spots for ' + str(self.amount_charged) + ' for trip ' + unicode(self.trip)
