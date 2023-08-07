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
            trains[train_id] = {
                'Train Name': train_name,
                'Source Station': source_station,
                'Destination Station': destination_station,
                'Total Seats': total_seats,
                'fare_per_seat': fare_per_seat,
                'Booked Seats': 0
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


def check_seat_availability(train, passenger):
    train_id = passenger['Train ID']
    num_tickets = passenger['Number of Tickets']

    if train_id not in train:
        raise ValueError(f"Invalid Train ID: {train_id}")

    available_seats = train[train_id]['Total Seats'] - train[train_id]['Booked Seats']
    if num_tickets > available_seats:
        raise ValueError(f"Insufficient Seats on Train {train_id}. Available Seats: {available_seats}")

    fare_per_ticket = train[train_id]['fare_per_seat']
    total_fare = num_tickets * fare_per_ticket

    return total_fare



def update_seat_availability(train, passenger):
    train_id = passenger['Train ID']
    num_tickets = passenger['Number of Tickets']

    train[train_id]['Booked Seats'] += num_tickets



def generate_report1(trains):
    print("Report 1: Details of all trains")
    print("{:<10} {:<15} {:<15} {:<15} {:<10}".format("Train ID", "Train Name", "Source Station", "Destination Station", "Total Seats"))
    for train_id, train_info in trains.items():
        print("{:<10} {:<15} {:<15} {:<15} {:<10}".format(train_id, train_info['Train Name'], train_info['Source Station'], train_info['Destination Station'], train_info['Total Seats']))

# Function to generate Report 2: Total revenue earned from each train
def generate_report2(trains):
    print("\nReport 2: Total revenue earned from each train")
    print("{:<10} {:<15} {:<15}".format("Train ID", "Train Name", "Total Revenue"))
    for train_id, train_info in trains.items():
        total_revenue = train_info['Booked Seats'] * train_info['fare_per_seat']
        print("{:<10} {:<15} {:<15}".format(train_id, train_info['Train Name'], total_revenue))

if __name__ == "__main__":
    try:
        trains = load_train_data()
        passengers = load_passenger_data()

        for passenger in passengers:
            total_fare = check_seat_availability(trains, passenger)
            print(f"\nBooking Confirmed: Passenger {passenger['Passenger Name']} for Train {passenger['Train ID']} - Tickets: {passenger['Number of Tickets']} - Fare: {total_fare}")
            update_seat_availability(trains, passenger)

        # Generate reports
        generate_report1(trains)
        generate_report2(trains)

    except Exception as e:
        print("Error:", e)
