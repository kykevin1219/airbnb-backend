from django.db    import models
from account.models import Users, HostInfos
   
class Beds(models.Model):
    bed_type = models.CharField(max_length = 50)

    class Meta:
        db_table = 'beds'

class RoomTypes(models.Model):
    room_type = models.CharField(max_length = 50)
    description = models.CharField(max_length = 200)

    class Meta:
        db_table = 'room_types'

class Amenities(models.Model):
    amenity = models.CharField(max_length = 50)

    class Meta:
        db_table = 'amenities'

class Rules(models.Model):
    rule = models.CharField(max_length = 100)
    
    class Meta:
        db_table = 'rules'

class RefundPolicies(models.Model):
    policy =      models.CharField(max_length = 50)
    description = models.TextField(max_length = 1000)

    class Meta:
        db_table = 'refund_policies'
class Cities(models.Model):
    city = models.CharField(max_length = 200)

    class Meta:
        db_table = 'cities'

class Cities(models.Model):
    city = models.CharField(max_length = 50)

    class Meta:
        db_table = 'cities'

class Rooms(models.Model):
    title =             models.CharField(max_length = 200)
    person_limit =      models.IntegerField()
    bed =               models.ManyToManyField(Beds, through = 'RoomsBeds')
    bathroom =          models.IntegerField()
    room_type =         models.ForeignKey(RoomTypes, on_delete = models.CASCADE)
    description =       models.TextField(max_length = 3000)
    amenity =           models.ManyToManyField(Amenities, through = 'RoomsAmenities')
    host =              models.ForeignKey(HostInfos, on_delete = models.CASCADE, null = True) 
    rules =             models.ManyToManyField(Rules, through = 'RoomsRules')
    refund_policy =     models.ForeignKey(RefundPolicies, on_delete = models.CASCADE)
    lat =               models.DecimalField(max_digits=9, decimal_places = 6, null = True)
    lng =               models.DecimalField(max_digits=9, decimal_places = 6, null = True)
    fee =               models.DecimalField(max_digits = 20, decimal_places = 2, null = True)
    cleaning_fee =      models.DecimalField(max_digits = 20, decimal_places = 2, null = True)
    city =              models.ForeignKey(Cities, on_delete = models.CASCADE, null = True)
    created_at =        models.DateTimeField(auto_now_add = True)
    updated_at =        models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'rooms'

class Pictures(models.Model):
    room =    models.ForeignKey(Rooms, on_delete = models.CASCADE)
    picture = models.URLField(max_length = 500)
    
    class Meta:
        db_table = 'pictures'

class RoomsBeds(models.Model):
    room = models.ForeignKey(Rooms, on_delete = models.CASCADE)
    bed =  models.ForeignKey(Beds, on_delete = models.CASCADE)
    number_of_beds = models.IntegerField()

    class Meta:
        db_table = 'rooms_beds'

class RoomsAmenities(models.Model):
    room =    models.ForeignKey(Rooms, on_delete = models.CASCADE)
    amenity = models.ForeignKey(Amenities, on_delete = models.CASCADE)

    class Meta:
        db_table = 'rooms_amenities'

class RoomsRules(models.Model):
    room = models.ForeignKey(Rooms, on_delete = models.CASCADE)
    rule = models.ForeignKey(Rules, on_delete = models.CASCADE)

    class Meta:
        db_table = 'rooms_rules'
