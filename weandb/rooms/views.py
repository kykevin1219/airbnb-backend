import json
import math
import requests

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Sum
from random           import sample
from decimal          import *
from operator         import itemgetter

from my_settings      import weandb_SECRET
from .models          import (
    Rooms,
    Pictures,
    RoomsBeds,
    RoomsAmenities,
    RoomsRules,
    Cities
)
from account.models   import (
    Users,
    HostInfos,
    HostInfosLanguages
)

class RoomView(View) :
    def get(self, request):
        offset         = int(request.GET.get('offset', 0))
        limit          = int(request.GET.get('limit', 20))
        counting_all   = Rooms.objects.all().count()
        selected_rooms = Rooms.objects.prefetch_related('pictures_set').all()[offset:limit]
        result_data    = [{
            "id"    : selected_room.id,
            "city"  : selected_room.city.city,
            "title" : selected_room.title,
            "pic1"  : selected_room.pictures_set.all()[0].picture,
            "pic2"  : selected_room.pictures_set.all()[1].picture,
            "pic3"  : selected_room.pictures_set.all()[2].picture,
            "pic4"  : selected_room.pictures_set.all()[3].picture,
            "pic5"  : selected_room.pictures_set.all()[4].picture
            } for selected_room in selected_rooms
        ]
        
        return JsonResponse({"rooms_list" : result_data, "total" : counting_all}, status = 200)

class DetailView(View) :
    def get(self, request, room_no):
        try :
            selected_room  = Rooms.objects.select_related('host', 'room_type', 'refund_policy').prefetch_related('pictures_set', 'roomsbeds_set').get(id = room_no)
            pics           = selected_room.pictures_set.values_list('picture',flat = True)
            beds           = selected_room.roomsbeds_set.aggregate(Sum("number_of_beds"))
            amenities      = selected_room.amenity.values_list('amenity', flat = True)
            rules          = selected_room.rules.values_list('rule', flat = True)
            host_languages = HostInfosLanguages.objects.select_related('language').filter(hostinfo_id = selected_room.host.id)
            language_list  = [
                host_language.language.language
                for host_language in host_languages
            ]
            result_data = {
                "id"            : selected_room.id,
                "pic1"          : pics[0],
                "pic2"          : pics[1],
                "pic3"          : pics[2],
                "pic4"          : pics[3],
                "pic5"          : pics[4],
                "city_name"     : selected_room.city.city,
                "name"          : selected_room.title,
                "hostpic"       : selected_room.host.host_image,
                "hostname"      : selected_room.host.nickname,
                "maxpeople"     : selected_room.person_limit,
                "bed"           : beds['number_of_beds__sum'],
                "bathroom"      : selected_room.bathroom,
                "roomtype"      : selected_room.room_type.room_type,
                "roomtypedesc"  : selected_room.room_type.description,
                "roomstory"     : selected_room.description,
                "utility_count" : len(amenities),
                "utility_list"  : list(amenities),
                "language_list" : language_list,
                "hostintro"     : selected_room.host.intro,
                "warning_list"  : list(rules),
                "refund_policy" : selected_room.refund_policy.policy,
                "refund_desc"   : selected_room.refund_policy.description,
                "price"         : selected_room.fee,
                "cleaning_fee"  : selected_room.cleaning_fee,
                "center"        : {
                    "lat" : selected_room.lat,
                    "lng" : selected_room.lng,
                }
            }

            return JsonResponse({"room_information" : result_data}, status = 200)

        except Rooms.DoesNotExist :
            return JsonResponse({"error" : "ROOM_NOT_FOUND"}, status = 404)

class RandomRecommendationView(View) :
    def get(self, request):
        number      = int(request.GET.get('number' , 2))
        offset      = int(request.GET.get('offset' , 0))
        limit       = int(request.GET.get('limit', 10))
        get_cities  = sample(list(Cities.objects.all()), number)
        city_names  = [get_city.city for get_city in get_cities]
        result_data = [{
            "city_name"        : get_city.city,
            "city_rooms_total" : Rooms.objects.filter(city_id = get_city.id).count(),
            "city_rooms"       :[
                {
                    "room_id"    : room.id,
                    "room_title" : room.title,
                    "room_city"  : room.city.city,
                    "room_pic1"  : room.pictures_set.values_list("picture", flat = True)[0],
                    "room_pic2"  : room.pictures_set.values_list("picture", flat = True)[1],
                    "room_pic3"  : room.pictures_set.values_list("picture", flat = True)[2],
                    "room_pic4"  : room.pictures_set.values_list("picture", flat = True)[3],
                    "room_pic5"  : room.pictures_set.values_list("picture", flat = True)[4]
            } for room in Rooms.objects.prefetch_related("pictures_set").filter(city_id = get_city.id)[offset:limit]]
        } for get_city in get_cities]
        
        return JsonResponse({"selected_data": result_data}, status = 200)

class CityRecommendationView(View) :
    def get(self, request):
        number      = int(request.GET.get('number', 10))
        get_cities  = sample(list(Cities.objects.all()), number)
        result_data = [{
            "city_id"       : get_city.id,
            "selected_city" : get_city.city
        } for get_city in get_cities]

        return JsonResponse({"result_data" : result_data}, status = 200)

class SearchView(View) :
    def get(self, request):
        keyword       = request.GET.get('keyword', '서울')
        get_info      = requests.get(f"""https://maps.googleapis.com/maps/api/geocode/json?address={keyword}&key={weandb_SECRET['google_geocoding_api']}""").json()
        input_lat     = get_info["results"][0]['geometry']['location']['lat']
        input_lng     = get_info["results"][0]['geometry']['location']['lng']
        offset        = int(request.GET.get('offset', 0))
        limit         = int(request.GET.get('limit', 5))
        all_rooms     = Rooms.objects.all()
        ids_distances = [{
            "room_id"  : room.id,
            "distance" : math.sqrt(((Decimal(room.lat) - Decimal(input_lat)) ** 2) +  ((Decimal(room.lng) - Decimal(input_lng)) ** 2))
        } for room in all_rooms]
        results_list     = sorted(ids_distances, key=itemgetter('distance'))[offset:limit]
        result_ids       = [result["room_id"] for result in results_list]
        result_instances = Rooms.objects.prefetch_related('pictures_set', 'roomsbeds_set').filter(id__in = result_ids)
        result_data      = [{
            "room_id"    : room.id,
            "room_title" : room.title,
            "room_city"  : room.city.city,
            "price"      : int(room.fee),
            "person"     : room.person_limit,
            "beds"       : room.roomsbeds_set.aggregate(Sum("number_of_beds"))['number_of_beds__sum'],
            "bathroom"   : room.bathroom,
            "amenities"  : list(room.amenity.values_list('amenity',flat = True)),
            "pic1"       : room.pictures_set.values_list('picture', flat = True)[0],
            "pic2"       : room.pictures_set.values_list('picture', flat = True)[1],
            "pic3"       : room.pictures_set.values_list('picture', flat = True)[2],
            "pic4"       : room.pictures_set.values_list('picture', flat = True)[3],
            "pic5"       : room.pictures_set.values_list('picture', flat = True)[4],
            "lat"        : room.lat,
            "lng"        : room.lng
        } for room in result_instances]

        return JsonResponse({"searched_results" : result_data}, status = 200)

class CitySearchView(View) :
    def get(self, request, city_no) :
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 5))
        city_rooms = Rooms.objects.filter(city_id = city_no)[offset:limit]
        result_data = [{
            "room_id"    : room.id,
            "room_title" : room.title,
            "room_city"  : room.city.city,
            "price"      : int(room.fee),
            "person"     : room.person_limit,
            "beds"       : room.roomsbeds_set.aggregate(Sum("number_of_beds"))['number_of_beds__sum'],
            "bathroom"   : room.bathroom,
            "amenities"  : list(room.amenity.values_list('amenity',flat = True)),
            "pic1"       : room.pictures_set.values_list('picture', flat = True)[0],
            "pic2"       : room.pictures_set.values_list('picture', flat = True)[1],
            "pic3"       : room.pictures_set.values_list('picture', flat = True)[2],
            "pic4"       : room.pictures_set.values_list('picture', flat = True)[3],
            "pic5"       : room.pictures_set.values_list('picture', flat = True)[4],
            "lat"        : room.lat,
            "lng"        : room.lng
        } for room in city_rooms]

        return JsonResponse({"searched_results" : result_data}, status = 200)
