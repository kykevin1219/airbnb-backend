import json

from django.test    import TestCase, Client

from .models        import (Beds, 
                            RoomTypes, 
                            Amenities,
                            Rules,
                            RefundPolicies,
                            Rooms,
                            Pictures,
                            RoomsBeds,
                            RoomsAmenities, 
                            RoomsRules,
                            Cities)
from account.models import (Users, 
                            Languages,
                            HostInfos, 
                            HostInfosLanguages, 
                            Languages)

class RoomViewTest(TestCase):
    maxDiff = None
    def setUp(self):
        user = Users.objects.create(
            id         = 1,
            first_name = "Tester",
            is_host    = True
        )
        language = Languages.objects.create(
            id       = 1,
            language = "Korean"
        )
        hostinfo = HostInfos.objects.create(
            id          = 1,
            host_image  = "http://www.naver.com",
            nickname    = "Tester Nickname",
            intro       = "Tester Introduction",
            interaction = "Tester Interaction",
            country     = "North Korea",
            city        = "Pyeongyang",
            user        = user,
        )
        HostInfosLanguages.objects.create(
            id       = 1,
            hostinfo = hostinfo,
            language = language
        )
        bed = Beds.objects.create(
           id       = 1,
           bed_type = "single"
        )
        roomtype = RoomTypes.objects.create(
            id          = 1,
            room_type   = "single",
            description = "single room"
        )
        amenity = Amenities.objects.create(
            id = 1,
            amenity = "iron man"
        )
        rule = Rules.objects.create(
            id   = 1,
            rule = "no pet"
        )
        refund_policy = RefundPolicies.objects.create(
            id          = 1,
            policy      = "flexible",
            description = "refundable before 1 day"
        )
        city = Cities.objects.create(
            id = 1,
            city = "seoul"
        )
        room = Rooms.objects.create(
            id            = 1 ,
            title         = "Test House",
            person_limit  = 4,
            bathroom      = 4,
            room_type     = roomtype,
            description   = "Test Description",
            host          = hostinfo,
            refund_policy = refund_policy,
            lat           = 30.000000,
            lng           = 60.000000,
            fee           = 30000.00,
            cleaning_fee  = 20000.00,
            city          = city
        )
        room_two = Rooms.objects.create(
            id            = 2,
            title         = "Test House 2",
            person_limit  = 4,
            bathroom      = 4,
            room_type     = roomtype,
            description   = "Test Description 2",
            host          = hostinfo,
            refund_policy = refund_policy,
            lat           = 30.000000,
            lng           = 60.000000,
            fee           = 30000.00,
            cleaning_fee  = 20000.00,
            city          = city
        )
        room_three = Rooms.objects.create(
            id            = 3,
            title         = "Test House 3",
            person_limit  = 4,
            bathroom      = 4,
            room_type     = roomtype,
            description   = "Test Description 3",
            host          = hostinfo,
            refund_policy = refund_policy,
            lat           = 30.000000,
            lng           = 60.000000,
            fee           = 30000.00,
            cleaning_fee  = 20000.00,
            city          = city
        )
        room_four = Rooms.objects.create(
            id            = 4,
            title         = "Test House 4",
            person_limit  = 4,
            bathroom      = 4,
            room_type     = roomtype,
            description   = "Test Description 4",
            host          = hostinfo,
            refund_policy = refund_policy,
            lat           = 30.000000,
            lng           = 60.000000,
            fee           = 30000.00,
            cleaning_fee  = 20000.00,
            city          = city
        )
        room_five = Rooms.objects.create(
            id            = 5,
            title         = "Test House 5",
            person_limit  = 4,
            bathroom      = 4,
            room_type     = roomtype,
            description   = "Test Description 5",
            host          = hostinfo,
            refund_policy = refund_policy,
            lat           = 30.000000,
            lng           = 60.000000,
            fee           = 30000.00,
            cleaning_fee  = 20000.00,
            city          = city
        )
        Pictures.objects.bulk_create([
            Pictures(id = 1, room = room, picture = "http://www.naver.com"),
            Pictures(id = 2, room = room, picture = "http://www.daum.net"),
            Pictures(id = 3, room = room, picture = "http://www.google.com"),
            Pictures(id = 4, room = room, picture = "https://wecode.co.kr/"),
            Pictures(id = 5, room = room, picture = "http://www.github.com"),
            Pictures(id = 6, room = room_two, picture = "http://www.naver.com"),
            Pictures(id = 7, room = room_two, picture = "http://www.naver.com"),
            Pictures(id = 8, room = room_two, picture = "http://www.naver.com"),
            Pictures(id = 9, room = room_two, picture = "http://www.naver.com"),
            Pictures(id = 10, room = room_two, picture = "http://www.naver.com"),
            Pictures(id = 11, room = room_three, picture = "http://www.daum.net"),
            Pictures(id = 12, room = room_three, picture = "http://www.daum.net"),
            Pictures(id = 13, room = room_three, picture = "http://www.daum.net"),
            Pictures(id = 14, room = room_three, picture = "http://www.daum.net"),
            Pictures(id = 15, room = room_three, picture = "http://www.daum.net"),
            Pictures(id = 16, room = room_four, picture = "http://www.google.com"),
            Pictures(id = 17, room = room_four, picture = "http://www.google.com"),
            Pictures(id = 18, room = room_four, picture = "http://www.google.com"),
            Pictures(id = 19, room = room_four, picture = "http://www.google.com"),
            Pictures(id = 20, room = room_four, picture = "http://www.google.com"),
            Pictures(id = 21, room = room_five, picture = "https://wecode.co.kr/"),
            Pictures(id = 22, room = room_five, picture = "https://wecode.co.kr/"),
            Pictures(id = 23, room = room_five, picture = "https://wecode.co.kr/"),
            Pictures(id = 24, room = room_five, picture = "https://wecode.co.kr/"),
            Pictures(id = 25, room = room_five, picture = "https://wecode.co.kr/")
        ])
        RoomsAmenities.objects.create(
            id =      1,
            amenity = amenity,
            room =    room
        )
        RoomsBeds.objects.create(
            id =             1,
            bed =            bed,
            room =           room,
            number_of_beds = 5
        )
        RoomsRules.objects.create(
            id =      1,
            room =    room,
            rule =    rule
        )

    def test_detail_view(self):
        c = Client()
        response = c.get('/rooms/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "room_information" : {
                    "id" :            1,
                    "pic1" :          "http://www.naver.com",
                    "pic2" :          "http://www.daum.net",
                    "pic3" :          "http://www.google.com",
                    "pic4" :          "https://wecode.co.kr/",
                    "pic5" :          "http://www.github.com",
                    "city_name" :     "seoul",
                    "name" :          "Test House",    
                    "hostpic" :       "http://www.naver.com",
                    "hostname" :      "Tester Nickname",
                    "maxpeople" :     4,
                    "bed" :           5,
                    "bathroom" :      4,
                    "roomtype" :      "single",
                    "roomtypedesc" :  "single room",
                    "roomstory"    :  "Test Description",
                    "utility_count" : 1,
                    "utility_list"  : ["iron man"],
                    "language_list" : ["Korean"],
                    "hostintro" :     "Tester Introduction",
                    "warning_list" :  ["no pet"],
                    "refund_policy" : "flexible",
                    "refund_desc" :   "refundable before 1 day",
                    "price" :         "30000.00",
                    "cleaning_fee" :  "20000.00",
                    "center" : {
                        "lat" : "30.000000",
                        "lng" : "60.000000",
                    }
                }
            }
        )

    def test_detail_view_fail(self):
        c = Client()
        response = c.get('/rooms/7')
        self.assertEqual(response.status_code, 404)

    def test_room_list_view_default(self):
        c = Client()
        response = c.get('/rooms', {'offset' : 0, 'limit' : 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"rooms_list" : [
                {
                "id" : 1,
                "city" : "seoul",
                "title" : "Test House",
                "pic1" : "http://www.naver.com",
                "pic2" : "http://www.daum.net",
                "pic3" : "http://www.google.com",
                "pic4" : "https://wecode.co.kr/",
                "pic5" : "http://www.github.com",
                },
                {
                "id" : 2,
                "city" : "seoul",
                "title" : "Test House 2",
                "pic1" : "http://www.naver.com",
                "pic2" : "http://www.naver.com",
                "pic3" : "http://www.naver.com",
                "pic4" : "http://www.naver.com",
                "pic5" : "http://www.naver.com",
                },
                {
                "id" : 3,
                "city" : "seoul",
                "title" : "Test House 3",
                "pic1" : "http://www.daum.net",
                "pic2" : "http://www.daum.net",
                "pic3" : "http://www.daum.net",
                "pic4" : "http://www.daum.net",
                "pic5" : "http://www.daum.net",
                },
                {
                "id" : 4,
                "city" : "seoul",
                "title" : "Test House 4",
                "pic1" : "http://www.google.com",
                "pic2" : "http://www.google.com",
                "pic3" : "http://www.google.com",
                "pic4" : "http://www.google.com",
                "pic5" : "http://www.google.com"
                },
                {
                "id" : 5,
                "city" : "seoul",
                "title" : "Test House 5",
                "pic1" : "https://wecode.co.kr/",
                "pic2" : "https://wecode.co.kr/",
                "pic3" : "https://wecode.co.kr/",
                "pic4" : "https://wecode.co.kr/",
                "pic5" : "https://wecode.co.kr/"
                }
            ], 
            "total" : 5
            }
        )
    
    def test_random_recommendation_view(self) :
        c = Client()
        response = c.get('/rooms/cityrecommendation', {'number' : 1, 'offset' : 0, 'limit' : 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"selected_data" :[
                {"city_name" : "seoul",
                 "city_rooms_total" : 5,
                 "city_rooms" :[
                     {
                         "room_id" : 1,
                         "room_title" : "Test House",
                         "room_city" : "seoul",
                         "room_pic1" : "http://www.naver.com", 
                         "room_pic2" : "http://www.daum.net",
                         "room_pic3" : "http://www.google.com",
                         "room_pic4" : "https://wecode.co.kr/",
                         "room_pic5" : "http://www.github.com"
                     },
                     {
                         "room_id" : 2,
                         "room_title" : "Test House 2",
                         "room_city" : "seoul",
                         "room_pic1" : "http://www.naver.com", 
                         "room_pic2" : "http://www.naver.com",
                         "room_pic3" : "http://www.naver.com",
                         "room_pic4" : "http://www.naver.com",
                         "room_pic5" : "http://www.naver.com"
                     },
                     {
                         "room_id" : 3,
                         "room_title" : "Test House 3",
                         "room_city" : "seoul",
                         "room_pic1" : "http://www.daum.net",
                         "room_pic2" : "http://www.daum.net",
                         "room_pic3" : "http://www.daum.net",
                         "room_pic4" : "http://www.daum.net",
                         "room_pic5" : "http://www.daum.net"
                     },
                     {
                         "room_id" : 4,
                         "room_title" : "Test House 4",
                         "room_city" : "seoul",
                         "room_pic1" : "http://www.google.com",
                         "room_pic2" : "http://www.google.com",
                         "room_pic3" : "http://www.google.com",
                         "room_pic4" : "http://www.google.com",
                         "room_pic5" : "http://www.google.com"
                     },
                     {
                         "room_id" : 5,
                         "room_title" : "Test House 5",
                         "room_city" : "seoul",
                         "room_pic1" : "https://wecode.co.kr/", 
                         "room_pic2" : "https://wecode.co.kr/",
                         "room_pic3" : "https://wecode.co.kr/",
                         "room_pic4" : "https://wecode.co.kr/",
                         "room_pic5" : "https://wecode.co.kr/"
                     }]
                }]
            })

    def test_city_recommendation_view(self) :
        c = Client()
        response = c.get('/rooms/cities', {'number' : 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"result_data" : [{
                "city_id" : 1,
                "selected_city" : "seoul"
                }]
            }
        )

    def test_search_view(self) : 
        c = Client()
        response = c.get('/rooms/search', {"keyword" : "seoul"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"searched_results" : [
                {
                    "room_id"    : 1,
                    "room_title" : "Test House",
                    "room_city"  : "seoul",
                    "price"      : 30000,
                    "person"     : 4,
                    "beds"       : 5,
                    "bathroom"   : 4,
                    "amenities"  : ["iron man"],
                    "pic1"       : "http://www.naver.com",
                    "pic2"       : "http://www.daum.net",
                    "pic3"       : "http://www.google.com",
                    "pic4"       : "https://wecode.co.kr/",
                    "pic5"       : "http://www.github.com",
                    "lat"        : "30.000000",
                    "lng"        : "60.000000",
                },
                {
                    "room_id"    : 2,
                    "room_title" : "Test House 2",
                    "room_city"  : "seoul",
                    "price"      : 30000,
                    "person"     : 4,
                    "beds"       : None,
                    "bathroom"   : 4,
                    "amenities"  : [],
                    "pic1"       : "http://www.naver.com",
                    "pic2"       : "http://www.naver.com", 
                    "pic3"       : "http://www.naver.com", 
                    "pic4"       : "http://www.naver.com",
                    "pic5"       : "http://www.naver.com",
                    "lat"        : "30.000000",
                    "lng"        : "60.000000",
                },
                {
                    "room_id"    : 3,
                    "room_title" : "Test House 3",
                    "room_city"  : "seoul",
                    "price"      : 30000,
                    "person"     : 4,
                    "beds"       : None,
                    "bathroom"   : 4,
                    "amenities"  : [],
                    "pic1"       : "http://www.daum.net",
                    "pic2"       : "http://www.daum.net",
                    "pic3"       : "http://www.daum.net",
                    "pic4"       : "http://www.daum.net",
                    "pic5"       : "http://www.daum.net",
                    "lat"        : "30.000000",
                    "lng"        : "60.000000",
                },
                {
                    "room_id"    : 4,
                    "room_title" : "Test House 4",
                    "room_city"  : "seoul",
                    "price"      : 30000,
                    "person"     : 4,
                    "beds"       : None,
                    "bathroom"   : 4,
                    "amenities"  : [],
                    "pic1"       : "http://www.google.com",
                    "pic2"       : "http://www.google.com",
                    "pic3"       : "http://www.google.com",
                    "pic4"       : "http://www.google.com",
                    "pic5"       : "http://www.google.com",
                    "lat"        : "30.000000",
                    "lng"        : "60.000000",
                },
                {
                    "room_id"    : 5,
                    "room_title" : "Test House 5",
                    "room_city"  : "seoul",
                    "price"      : 30000,
                    "person"     : 4,
                    "beds"       : None,
                    "bathroom"   : 4,
                    "amenities"  : [],
                    "pic1"       : "https://wecode.co.kr/",
                    "pic2"       : "https://wecode.co.kr/", 
                    "pic3"       : "https://wecode.co.kr/",
                    "pic4"       : "https://wecode.co.kr/",
                    "pic5"       : "https://wecode.co.kr/",
                    "lat"        : "30.000000",
                    "lng"        : "60.000000",
                },

            ]
            }
            )
