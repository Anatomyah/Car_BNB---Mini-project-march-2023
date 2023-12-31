from abc import ABC
from datetime import datetime
from config import *
from filehandler import FileHandler
from helpers import get_by_id, is_available
from car import Car
from person import Person


class Rent(FileHandler, ABC):
    __ID_COUNTER = 0 # Static variable to track the rental order ID

    def __init__(self, pickup_time, return_time, client, car):
        """
              Initializes a new Rent object.

              Parameters:
                  pickup_time (str): The pickup time for the rental.
                  return_time (str): The return time for the rental.
                  client (int): The ID of the client renting the car.
                  car (int): The serial number of the car being rented.
              """
        Rent.get_id_counter()  # Retrieving the current ID counter value

        self.id = Rent.__ID_COUNTER  # Setting the rental order ID
        self.pickup_time = pickup_time
        self.return_time = return_time
        self.client = client
        self.car = car

        Rent.__ID_COUNTER += 1  # Incrementing the ID counter
        Rent.save_id_counter()  # Saving the updated counter to file

    # Static methods for managing the ID counter

    @staticmethod
    def get_id_counter():
        # Code to retrieve the ID counter from file ...
        with open(RENT_ID_COUNTER, 'r') as fh:
            Rent.__ID_COUNTER = int(fh.read())

    @staticmethod
    def save_id_counter():
        # Code to save the ID counter to file ...
        with open(RENT_ID_COUNTER, 'w') as fh:
            fh.write(str(Rent.__ID_COUNTER))

    # Methods for representing the object as a string or a dictionary
    def obj_to_str(self):
        return f"{self.id},{self._pickup_time},{self._return_time},{self._client.id},{self._car.serial}"

    def obj_to_dict(self):
        return {'ID': self.id, 'Pickup Time': self._pickup_time, 'Return Time': self._return_time,
                'Client': self._client.id, 'Car': self._car.serial}

    def show(self):
        """
               Displays the details of the rental order.
               """
        print(f"\n*** Order Details ***\n"
              f"Order ID: {self.id}\n"
              f"Pickup Time: {self._pickup_time}\n"
              f"Return Time: {self._return_time}\n"
              f"Client: {self._client.id}\n"
              f"Car: {self._car.serial}")

    def get_file_path(self, fieldnames=False):
        # Code to get the file path for rental data ...
        res = RENT_PATH

        if fieldnames:
            res = {'file_path': RENT_PATH, 'fieldnames': RENT_FIELDNAMES}

        return res

    def get_id(self):
        """
        Returns the ID of the rental order.

        Returns:
            int: The ID of the rental order.
        """
        return self.id

    # Properties and setters for various attributes like pickup_time, return_time, car, and client
    @property
    def pickup_time(self):
        # Getter for pickup_time ...
        return self._pickup_time

    @pickup_time.setter
    def pickup_time(self, new_val):
        # Setter for pickup_time with validation ...
        assert not any(x.isalpha() for x in new_val), f"Invalid date. " \
                                                                             f"Date ust be in the YYYY-MM-DD format " \
                                                                             f"cannot contain letters or be under 6 " \
                                                                             f"characters"

        date_object = datetime.strptime(new_val, '%Y-%m-%d %H:%M:%S')

        self._pickup_time = date_object

    # Similar property and setter definitions for return_time, car, client
    @property
    def return_time(self):
        return self._return_time

    @return_time.setter
    def return_time(self, new_val):
        assert not any(x.isalpha() for x in new_val), f"Invalid date. " \
                                                                             f"Date ust be in the YYYY-MM-DD format " \
                                                                             f"cannot contain letters or be under 6 " \
                                                                             f"characters"

        date_object = datetime.strptime(new_val, '%Y-%m-%d %H:%M:%S')

        self._return_time = date_object
        assert is_available(self) is not False, "Chosen vehicle is already taken within the desired time frame"

    @property
    def car(self):
        return self._car

    @car.setter
    def car(self, new_val):
        assert len(new_val) > 6 and not any(x.isalpha() for x in new_val), f"Invalid ID number. " \
                                                                           f"Number cannot contain letters or be " \
                                                                           f"under 6 characters"

        row = get_by_id(new_val, CARS_PATH)
        assert row is not None, f"This car Serial Number does not exists in our database"

        self._car = Car(row['Serial'], row['Brand'], row['Model'], row['Year'],
                        row['Engine'], row['Day Cost'], row['KM'], row['Owner'])

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, new_val):
        assert len(new_val) > 6 and not any(x.isalpha() for x in new_val), f"Invalid ID number. " \
                                                                           f"Number cannot contain letters or be " \
                                                                           f"under 6 characters"
        row = get_by_id(new_val, PERSON_PATH)
        assert row is not None, f"This client ID does not exists in our database"

        self._client = Person(row['ID'], row['First Name'], row['Last Name'], row['Age'], row['Email'],
                              row['Phone'])

    def rent_cost(self):
        """
               Calculates the cost of the rental.

               Returns:
                   int: The total cost of the rental.
               """
        days = self._return_time - self._pickup_time
        return days.days * self.car.day_cost

    @classmethod
    def load_from_csv(cls):
        """
            Loads rent objects from a CSV file.

            Returns:
                list of Rent: A list of rent objects loaded from the file.
            """
        reader = FileHandler.load(file_path=RENT_PATH)

        objects = []
        for row in reader:
            objects.append(cls(pickup_time=row['Pickup Time'],
                               return_time=row['Return Time'],
                               client=int(row['Client']),
                               car=int(row['Car'])))

        return objects
