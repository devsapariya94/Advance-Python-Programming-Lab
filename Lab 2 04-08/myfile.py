import csv


def load_train_data():
    trains = {}
    with open('trains.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            train_id = row['Train ID']
            train_name = row['Train Name']
            source_station = row['Source Station']
            destination_station = row['Destination Station']
            total_seats = int(row['Total Seats'])  
            fare_per_seat = int(row['fareperseat'])  
            booked_seats = int(row['Booked Seats']) if 'Booked Seats' in row else 0
            trains[train_id] = {
                'Train Name': train_name,
                'Source Station': source_station,
                'Destination Station': destination_station,
                'Total Seats': total_seats,
                'fare_per_seat': fare_per_seat,
                'Booked Seats': booked_seats
            }
    return trains


def load_passenger_data():
    passengers = []
    with open('passengers.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            passenger_name = row['Passenger Name']
            train_id = row['Train ID']
            num_tickets = int(row['Number of Tickets'])
            passengers.append({
                'Passenger Name': passenger_name,
                'Train ID': train_id,
                'Number of Tickets': num_tickets
            })
    return passengers


def check_seat_availability(trains, train_id, no_of_passenger):
    if train_id not in trains:
        print(f"Invalid Train ID: {train_id}")
        return False

    available_seats = trains[train_id]['Total Seats'] - trains[train_id]['Booked Seats']
    if no_of_passenger > available_seats:
        print(f"Insufficient Seats on Train {train_id}. Available Seats: {available_seats}")
        print("Please try again with a different train or lower number of passengers")
        print("---------------------------------------------------------------------------------------")
        return False

    return True


def update_seat_availability(trains, train_id, no_of_passenger):
    trains[train_id]['Booked Seats'] += no_of_passenger


def menu():
    print("Welcome to the Railway Reservation System")
    print("1. Book Ticket")
    print("2. Cancel Ticket")
    print("3. Show All Train Details")
    print("4. Exit")
    print("5. Revenue")
    print("6. Get Detailed Summary in text file")
    choice = int(input("Enter your choice: "))
    return choice


def add_new_passenger(passenger_name, train_id, no_of_passenger):
    with open('passengers.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Passenger Name', 'Train ID', 'Number of Tickets'])
        writer.writerow({
            'Passenger Name': passenger_name,
            'Train ID': train_id,
            'Number of Tickets': no_of_passenger
        })


def book_ticket(trains):
    train_id = input("Enter the Train ID: ")
    train = trains.get(train_id)
    if train is None:
        print(f"Invalid Train ID: {train_id}")
        return

    no_of_passenger = int(input("Enter the number of passengers: "))
    if check_seat_availability(trains, train_id, no_of_passenger):
        print("Seats are available")
        name_of_passenger = input("Enter the name of the passenger: ")
        print("Summary")
        print(f"Train ID: {train_id}")
        print(f"Train Name: {train['Train Name']}")
        print(f"Number of Passengers: {no_of_passenger}")
        print(f"Name of Passenger: {name_of_passenger}")
        print(f"Total Fare: {no_of_passenger * train['fare_per_seat']}")
        confirm = input("Confirm Booking (y/n): ")
        if confirm.lower() == 'y':
            update_seat_availability(trains, train_id, no_of_passenger)
            add_new_passenger(name_of_passenger, train_id, no_of_passenger)
            print("Ticket Booked Successfully")
        else:
            print("Ticket Booking Cancelled")


def cancel_ticket(trains):
    print("Cancel Ticket")
    passenger_name = input("Enter the name of the passenger: ")
    train_id = input("Enter the Train ID: ")

    with open('passengers.csv', mode='r') as file:
        reader = csv.DictReader(file)
        passengers = []
        found = False
        for row in reader:
            if row['Passenger Name'] == passenger_name and row['Train ID'] == train_id:
                found = True
                num_tickets = int(row['Number of Tickets'])
                continue

            passengers.append(row)

        if not found:
            print("Invalid Passenger Name or Train ID")
            return

    with open('passengers.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Passenger Name', 'Train ID', 'Number of Tickets'])
        writer.writeheader()
        for passenger in passengers:
            writer.writerow(passenger)
    trains[train_id]['Booked Seats'] -= num_tickets
    print("Ticket Cancelled Successfully")


def show_all_train_details(trains):
    print("Train Details")
    print("---------------------------------------------------------------------------------------")
    for train_id, train in trains.items():
        print(f"Train ID: {train_id}")
        print(f"Train Name: {train['Train Name']}")
        print(f"Source Station: {train['Source Station']}")
        print(f"Destination Station: {train['Destination Station']}")
        print(f"Total Seats: {train['Total Seats']}")
        print(f"Seats Booked: {train['Booked Seats']}")
        print(f"Fare per Seat: {train['fare_per_seat']}")
        print("---------------------------------------------------------------------------------------")


def revenue(trains):
    print("Revenue")
    print("---------------------------------------------------------------------------------------")
    total_revenue = 0
    for train_id, train in trains.items():
        revenue = train['Booked Seats'] * train['fare_per_seat']
        total_revenue += revenue
        print(f"Train ID: {train_id}")
        print(f"Train Name: {train['Train Name']}")
        print(f"Seats Booked: {train['Booked Seats']}")
        print(f"Revenue: {revenue}")
        print("---------------------------------------------------------------------------------------")
    print(f"Total Revenue: {total_revenue}")
    

def get_detailed_summary(trains):
    with open("summary.txt", "w") as file:
        file.write("All trains\n")
        for train_id, train in trains.items():
            file.write(f"Train ID: {train_id}\n")
            file.write(f"Train Name: {train['Train Name']}\n")
            file.write(f"Source Station: {train['Source Station']}\n")
            file.write(f"Destination Station: {train['Destination Station']}\n")
            file.write(f"Total Seats: {train['Total Seats']}\n")
            file.write(f"Seats Booked: {train['Booked Seats']}\n")
            file.write(f"Fare per Seat: {train['fare_per_seat']}\n")
            file.write(f"Total revenue: {train['Booked Seats'] * train['fare_per_seat']}\n")
            file.write("--------------------------------------------------\n")
        



    print("Detailed summary written to summary.txt")

# After calling main_menu(), you can call get_detailed_summary(trains) to generate the summary.


def main_menu():
    trains = load_train_data()
    passengers = load_passenger_data()
    while True:
        choice = menu()
        if choice == 1:
            book_ticket(trains)
        elif choice == 2:
            cancel_ticket(trains)
        elif choice == 3:
            show_all_train_details(trains)
        elif choice == 4:
            break
        elif choice == 5:
            revenue(trains)
        elif choice == 6:
            get_detailed_summary(trains)
        else:
            print("Invalid Choice")
        print("---------------------------------------------------------------------------------------")
    get_detailed_summary(trains)
    print("Thank you for using the Railway Reservation System")


main_menu()
