import json

from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from datetime import date
from decimal import Decimal

from .models import Reservations
from rooms.models import Rooms
from account.models import Users, HostInfos
from account.utils import login_required

class ReservationView(View) :
    @login_required
    def post(self, request) :
        data             = json.loads(request.body)
        user             = request.user.id
        room             = data["room_id"]
        host             = Rooms.objects.get(id = room).host_id
        check_in_date    = date(int(data["S_year"]), int(data["S_month"]), int(data["S_day"]))
        check_out_date   = date(int(data["E_year"]), int(data["E_month"]), int(data["E_day"]))
        reservations = Reservations.objects.filter(room_id = room)
        for reservation in reservations :
            if (check_in_date <= reservation.check_in < check_out_date) \
               or (check_in_date < reservation.check_out <= check_out_date) : 
                return JsonResponse({"error" : "RESERVATION_OVERLAPS"}, status = 409)
        Reservations.objects.create(
            guest_id  = user,
            room_id   = room,
            check_in  = check_in_date,
            check_out = check_out_date,
            host_id   = host
        )
        return JsonResponse({"message" : "RESERVATION_SUCCESS"}, status = 200)  

class ReservationListView(View) :
    @login_required
    def get(self, request) :
        offset       = int(request.GET.get('offset', 0))
        limit        = int(request.GET.get('limit', 5))
        user_id      = request.user.id
        reservations = Reservations.objects.filter(guest_id = user_id).order_by('-created_at')[offset:limit]
        result_data = [{
            "reservation_id"  : reservation.id,
            "room_id"         : reservation.room_id,
            "room_picture"    : reservation.room.pictures_set.all()[0].picture,
            "check_in_year"   : reservation.check_in.year,
            "check_in_month"  : reservation.check_in.month,
            "check_in_day"    : reservation.check_in.day,
            "check_out_year"  : reservation.check_out.year,
            "check_out_month" : reservation.check_out.month,
            "check_out_day"   : reservation.check_out.day,
            "price"           : str((reservation.room.fee * ((reservation.check_out - reservation.check_in).days)) * Decimal(1.05) + reservation.room.cleaning_fee).split('.')[0], 
            "refund_desc"     : reservation.room.refund_policy.description,
            "confirmation"    : reservation.is_confirmed
        }for reservation in reservations]
        
        return JsonResponse({"reservation_data" : result_data }, status = 200)

class ReservationHostView(View) :
    @login_required
    def get(self, request) :
        host = HostInfos.objects.get(user_id = request.user.id)
        reservations = Reservations.objects.filter(host_id = host.id).order_by('-created_at')
        result_data = [{
            "reservation_id" : reservation.id,
            "room_id" : reservation.room_id,
            "room_title" : reservation.room.title,
            "room_picture" : reservation.room.pictures_set.all()[0].picture,
            "check_in_year"   : reservation.check_in.year,
            "check_in_month"  : reservation.check_in.month,
            "check_in_day"    : reservation.check_in.day,
            "check_out_year"  : reservation.check_out.year,
            "check_out_month" : reservation.check_out.month,
            "check_out_day"   : reservation.check_out.day,
            "guest_name"      : reservation.guest.first_name,
            "guest_number"    : reservation.room.person_limit,
            "is_confirmed"    : reservation.is_confirmed
        } for reservation in reservations]

        return JsonResponse({"reservation_data" : result_data}, status = 200)

class ConfirmView(View) :
    @login_required
    def post(self, request) :
        host = HostInfos.objects.get(user_id = request.user.id)
        data = json.loads(request.body)
        reservation = Reservations.objects.get(id = data["reservation_id"])
        reservation.is_confirmed = True
        reservation.save()

        return JsonResponse({"message" : "RESERVATION_CONFIRMED"}, status = 200)
