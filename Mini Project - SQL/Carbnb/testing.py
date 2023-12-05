import unittest
from rent import Rent
from car import Car
from person import Person


class MyTestCase(unittest.TestCase):

    def test_person(self):
        # create a Person object, make sure in DB and delete
        p = Person(id_=123456789, p_name='Test', l_name='Testing', age=20, email='mashu@mashu.com', phone='0501234567')
        if self.assertIsInstance(p, Person, "Person object created successfully"):
            if self.assertTrue(p.save(), "Save Successful"):
                if self.assertIsNotNone(p.check_id(), "Object found in Database."):
                    self.assertTrue(p.delete(), 'Object deleted from Database.')

    def test_car(self):
        # create a Car object, make sure in DB and delete
        p = Person(id_=123456789, p_name='Test', l_name='Testing', age=20, email='mashu@mashu.com', phone='0501234567')
        p.save()

        c = Car(id_=123456789, brand='Test', model='Testing', year=2023,
                engine=1600, day_cost=600, km=2000, owner='123456789')

        if self.assertIsInstance(c, Car, "Car object created successfully"):
            if self.assertTrue(c.save(), "Save Successful"):
                if self.assertIsNotNone(c.check_id(), "Object found in Database."):
                    self.assertTrue(c.delete(), 'Object deleted from Database')

        p.delete()

    def test_rent(self):
        # Create rent object, make sure in DB and delete
        p = Person(id_=123456789, p_name='Test', l_name='Testing', age=20, email='mashu@mashu.com', phone='0501234567')
        p.save()
        c = Car(id_=123456789, brand='Test', model='Testing', year=2023,
                engine=1600, day_cost=600, km=2000, owner='123456789')
        c.save()

        r = Rent(pickup_time='2023-12-30 00:00:00', return_time='2023-12-31 00:00:00',
                 client='123456789', car='123456789', id_=1234, override=True)

        if self.assertIsInstance(r, Rent, "Rent object created successfully"):
            if self.assertTrue(r.save(), "Save Successful"):
                if self.assertIsNotNone(r.check_id(), "Object found in Database"):
                    self.assertTrue(r.delete(), 'Object deleted from Database')

        c.delete()
        p.delete()

    def test_rent_date(self):
        # create 2 orders with the same date - make sure an error is returned
        p = Person(id_=123456789, p_name='Test', l_name='Testing', age=20, email='mashu@mashu.com', phone='0501234567')
        p.save()
        c = Car(id_=123456789, brand='Test', model='Testing', year=2023,
                engine=1600, day_cost=600, km=2000, owner='123456789')
        c.save()

        r1 = Rent(pickup_time='2023-12-30 00:00:00', return_time='2023-12-31 00:00:00',
                  client='123456789', car='123456789', id_=1234, override=True)
        r1.save()
        with self.assertRaises(AssertionError):
            Rent(pickup_time='2023-12-30 00:00:00', return_time='2023-12-31 00:00:00',
                 client='123456789', car='5579699', id_=1234, override=True)

        r1.delete()
        c.delete()
        p.delete()

    def test_del_client_with_order(self):
        # Try to delete a client with an open order and make sure to receive error
        p = Person(id_=123456789, p_name='Test', l_name='Testing', age=20, email='mashu@mashu.com', phone='0501234567')
        p.save()
        c = Car(id_=123456789, brand='Test', model='Testing', year=2023,
                engine=1600, day_cost=600, km=2000, owner='123456789')
        c.save()
        r = Rent(pickup_time='2023-12-30 00:00:00', return_time='2023-12-31 00:00:00',
                 client='123456789', car='123456789', id_=1234, override=True)
        r.save()

        with self.assertRaises(AssertionError):
            p.delete()

        r.delete()
        c.delete()
        p.delete()

    def test_del_car_with_order(self):
        # Try to delete a client with an open order and make sure to receive error
        p = Person(id_=123456789, p_name='Test', l_name='Testing', age=20, email='mashu@mashu.com', phone='0501234567')
        p.save()
        c = Car(id_=123456789, brand='Test', model='Testing', year=2023,
                engine=1600, day_cost=600, km=2000, owner='123456789')
        c.save()
        r = Rent(pickup_time='2023-12-30 00:00:00', return_time='2023-12-31 00:00:00',
                 client='123456789', car='123456789', id_=1234, override=True)
        r.save()

        with self.assertRaises(AssertionError):
            c.delete()

        r.delete()
        c.delete()
        p.delete()


if __name__ == '__main__':
    unittest.main()
