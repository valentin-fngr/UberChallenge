from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from trips.models import Trip


PASSWORD = "passwOrd!"


def create_user(username, password, first_name, last_name):
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    user.save()
    return user

def create_trip(from_user=None, driver=None, pickup_address="Adress A", dropoff_address="Address B"):
    trip, _ = Trip.objects.get_or_create(
        from_user=from_user,
        driver=driver,
        pickup_address=pickup_address,
        dropoff_address=dropoff_address
    )
    trip.save()
    return trip


class TripTests(APITestCase):

    def setUp(self):
        user = create_user(
            "driver@test.com",
            PASSWORD,
            "test",
            "Mr Test"
        )
        response = self.client.post(reverse("login"), {"username": user.username, "password" : PASSWORD})
        self.access = response.data["access"]

    def test_can_retrieve_trips_list(self):
        trips = [
            Trip.objects.create(pickup_address="Pickup 1", dropoff_address="Pickup 1.1"),
            Trip.objects.create(pickup_address="Pickup 2", dropoff_address="Pickup 2.1")
        ]
        actual_id = [trip.id for trip in trips]
        url = reverse("list_trip")
        response = self.client.get(url, HTTP_AUTHORIZATION='Bearer '+ self.access)
        expected_id = [trip["id"] for trip in response.data]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(actual_id, expected_id)

    def test_can_retrieve_trip_by_id(self):
        trip = create_trip()
        trip_id = trip.id
        url = reverse("trip_detail", args=[trip_id])
        response = self.client.get(url, HTTP_AUTHORIZATION='Bearer '+ self.access)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], trip.id)
        self.assertEqual(response.data["pickup_address"], trip.pickup_address)
