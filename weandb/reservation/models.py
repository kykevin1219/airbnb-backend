from django.db import models
from account.models import Users, HostInfos
from rooms.models import Rooms

class Reservations(models.Model) :
    guest = models.ForeignKey(Users, on_delete = models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete = models.CASCADE)
    check_in = models.DateField(null = True)
    check_out = models.DateField(null = True)
    host = models.ForeignKey(HostInfos, on_delete = models.CASCADE, null = True)
    is_confirmed = models.BooleanField(null = True, default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta : 
        db_table = 'reservations'
