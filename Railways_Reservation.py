import random
import csv
import sys

logged_in = False  # global variable
uid = 0
pwd = ''


class train:
    def __init__(self, name='', num=0, arr_time='', dep_time='', src='', des='', day_of_travel='',
                 seat_available_in_1AC=0, seat_available_in_2AC=0, seat_available_in_SL=0, fare_1ac=0, fare_2ac=0,
                 fare_sl=0):
        self.name = name
        self.num = num
        self.arr_time = arr_time
        self.dep_time = dep_time
        self.src = src
        self.des = des
        self.day_of_travel = day_of_travel
        self.seats = {'1AC': seat_available_in_1AC, '2AC': seat_available_in_2AC, 'SL': seat_available_in_SL}
        self.fare = {'1AC': fare_1ac, '2AC': fare_2ac, 'SL': fare_sl}

    def print_seat_availablity(self):
        print("No. of seats available in 1AC :- " + str(self.seats['1AC']))
        print("No. of seats available in 2AC :- " + str(self.seats['2AC']))
        print("No. of seats available in SL :- " + str(self.seats['SL']))

    def check_availabilty(self, coach='', ticket_num=0):
        coach = coach.upper()
        if coach not in ('SL', '1AC', '2AC'):
            self.print_seat_availablity()
            coach = input("Enter the coach(1AC/2AC/SL) :-")
        else:
            if self.seats[coach] == 0:
                return False
            elif self.seats[coach] >= ticket_num:
                return True
            else:
                return False

    def book_ticket(self, coach='', no_of_tickets=0):
        self.seats[coach] -= no_of_tickets
        return True
    
    def modify_train(train_num):
        if train_num in trains:
            trains[train_num].name = input("Enter new train name: ")
            trains[train_num].seat_available_in_SL = int(input("Update SL seats: "))

        # Save trains to CSV
        save_trains_to_csv()


def save_tickets_to_csv():
    with open("tickets.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=['pnr', 'train_num', 'coach', 'uid', 'ticket_num'])
        writer.writeheader()
        for pnr, ticket_obj in ticket_dict.items():
            writer.writerow({
                'pnr': pnr,
                'train_num': ticket_obj.train_num,
                'coach': ticket_obj.coach,
                'uid': ticket_obj.uid,
                'ticket_num': ticket_obj.ticket_num
            })


class ticket:
    def __init__(self, train, user, ticket_num, coach):
        self.pnr = str(train.num) + str(user.uid) + str(random.randint(100, 999))
        self.train_num = train.num
        self.coach = coach
        self.uid = user.uid
        self.train_name = train.name
        self.user_name = user.name
        self.ticket_num = ticket_num
        user.history.update({self.pnr: self})
        ticket_dict.update({self.pnr: self})

        # Save tickets to CSV
        save_tickets_to_csv()


class user:
    def __init__(self, uid=0, name='', hometown='', cell_num='', pwd=''):
        self.uid = uid
        self.name = name
        self.hometown = ''
        self.cell_num = ''
        self.pwd = pwd
        self.history = {}


class acceptors:
    ''' Class containing functions for accepting and
	validating values properly'''

    def accept_uid():
        uid = 0
        try:
            uid = int(input("Enter the User ID:- "))
        except ValueError:
            print("Please enter user ID properly.")
            return acceptors.accept_uid()
        else:
            return uid

    def accept_pwd():
        pwd = input("Enter your password:- ")
        return pwd

    def accept_train_number():
        train_num = 0
        try:
            train_num = int(input("Enter the train number :- "))
        except ValueError:
            print("Please enter train number properly.")
            return acceptors.accept_train_number()
        else:
            if train_num not in trains:
                print("Please enter a valid train number.")
                return acceptors.accept_train_number()
            else:
                return train_num

    def accept_menu_option():
        option = input("Enter your option :- ")
        if option not in ('1', '2', '3', '4', '5', '6', '7', '8'):
            print("Please enter a valid option!")
            return acceptors.accept_menu_option()
        else:
            return int(option)

    def accept_coach():
        coach = input("Enter the coach :- ")
        coach = coach.upper()
        if coach not in ('SL', '1AC', '2AC'):
            print("Please enter coach properly.")
            return acceptors.accept_coach()
        else:
            return coach

    def accept_prompt():
        prompt = input("Confirm? (y/n) :-")
        if prompt not in ('y', 'n'):
            print("Please enter proper choice.")
            return acceptors.accept_prompt()
        return prompt

    def accept_ticket_num():
        ticket_num = 0
        try:
            ticket_num = int(input("Enter the number of tickets :- "))
            if ticket_num < 0:
                raise ValueError
        except ValueError:
            print("Enter proper ticket number.")
            return acceptors.accept_ticket_num()
        else:
            return ticket_num

    def accept_pnr():
        pnr = input("Enter your PNR number :- ")
        if pnr not in ticket_dict:
            print("Please enter proper PNR number :- ")
            return acceptors.accept_pnr()
        else:
            return pnr


def book_ticket():
    if not logged_in:
        login('p')

    check_seat_availabilty('p')
    choice = acceptors.accept_train_number()
    trains[choice].print_seat_availablity()
    coach = acceptors.accept_coach()
    ticket_num = acceptors.accept_ticket_num()
    if trains[choice].check_availabilty(coach, ticket_num):
        print("You have to pay :- ", trains[choice].fare[coach] * ticket_num, "  ")
        prompt = acceptors.accept_prompt()
        if prompt == 'y':
            trains[choice].book_ticket(coach, ticket_num)
            print("Booking Successful!\n\n")
            tick = ticket(trains[choice], users[uid], ticket_num, coach)
            print("Please note PNR number :- ", tick.pnr, "\n\n")
            menu()
        else:
            print("Exiting...\n\n")
            menu()
    else:
        print(ticket_num, " tickets not available")
        menu()


def cancel_ticket():
    pnr = acceptors.accept_pnr()
    if pnr in ticket_dict:
        check_pnr(pnr)
        print("Cancel the tickets?")
        prompt = acceptors.accept_prompt()
        if prompt == 'y':
            if logged_in:
                print("Ticket Cancelled.\n")
                trains[ticket_dict[pnr].train_num].seats[ticket_dict[pnr].coach] += ticket_dict[pnr].ticket_num
                del users[ticket_dict[pnr].uid].history[pnr]
                del ticket_dict[pnr]
                
                # Save changes to the CSV file
                save_tickets_to_csv()
            else:
                login('p')
                print("Ticket Cancelled.\n")
                trains[ticket_dict[pnr].train_num].seats[ticket_dict[pnr].coach] += ticket_dict[pnr].ticket_num
                del users[ticket_dict[pnr].uid].history[pnr]
                del ticket_dict[pnr]
                
                # Save changes to the CSV file
                save_tickets_to_csv()
        else:
            print("\nTicket not cancelled\n")
    menu()



def check_seat_availabilty(flag=''):
    src = input("Enter the source station:- ")
    des = input("Enter the destination station:- ")
    flag_2 = 0
    for i in trains:
        if trains[i].src == src and trains[i].des == des:
            print("Train Name :- ", trains[i].name, " ", "Number ", trains[i].num, " ", "Day of Travel :- ",
                  trains[i].day_of_travel)
            flag_2 += 1
    if flag_2 == 0:
        print("\nNo trains found between the stations you entered.\n")
        menu()
    if flag == '':
        train_num = acceptors.accept_train_number()
        trains[train_num].print_seat_availablity()
        menu()
    else:
        pass


def check_pnr(pnr=''):
    if pnr == '':
        pnr = acceptors.accept_pnr()
        print()
        print("User name:- ", ticket_dict[pnr].user_name)
        print("Train name:- ", ticket_dict[pnr].train_name)
        print("Train number:- ", ticket_dict[pnr].train_num, " Source:- ", trains[ticket_dict[pnr].train_num].src,
              " Destination:- ", trains[ticket_dict[pnr].train_num].des)
        print("No. of Tickets Booked :- ", ticket_dict[pnr].ticket_num)
        print()
        menu()
    else:
        print()
        print("User name:- ", ticket_dict[pnr].user_name)
        print("Train name:- ", ticket_dict[pnr].train_name)
        print("Train number:- ", ticket_dict[pnr].train_num, " Source:- ", trains[ticket_dict[pnr].train_num].src,
              " Destination:- ", trains[ticket_dict[pnr].train_num].des)
        print("No. of Tickets Booked :- ", ticket_dict[pnr].ticket_num)
        print()


def save_trains_to_csv():
    with open("trains.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            'num', 'name', 'arr_time', 'dep_time', 'src', 'des', 'day_of_travel',
            'seat_available_in_1AC', 'seat_available_in_2AC', 'seat_available_in_SL',
            'fare_1AC', 'fare_2AC', 'fare_SL'
        ])
        writer.writeheader()
        for train_obj in trains.values():
            writer.writerow({
                'num': train_obj.num,
                'name': train_obj.name,
                'arr_time': train_obj.arr_time,
                'dep_time': train_obj.dep_time,
                'src': train_obj.src,
                'des': train_obj.des,
                'day_of_travel': train_obj.day_of_travel,
                'seat_available_in_1AC': train_obj.seats['1AC'],
                'seat_available_in_2AC': train_obj.seats['2AC'],
                'seat_available_in_SL': train_obj.seats['SL'],
                'fare_1AC': train_obj.fare['1AC'],
                'fare_2AC': train_obj.fare['2AC'],
                'fare_SL': train_obj.fare['SL']
            })


def save_users_to_csv():
    with open("users.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=['uid', 'name', 'hometown', 'cell_num', 'pwd'])
        writer.writeheader()
        for user_obj in users.values():
            writer.writerow({
                'uid': user_obj.uid,
                'name': user_obj.name,
                'hometown': user_obj.hometown,
                'cell_num': user_obj.cell_num,
                'pwd': user_obj.pwd
            })


def create_new_acc():
    user_name = input("Enter your user name:- ")
    pwd = input("Enter your password :- ")
    uid = random.randint(1000, 9999)
    hometown = input("Enter your hometown :- ")
    cell_num = input("Enter your phone number :- ")
    u = user(uid, user_name, hometown, cell_num, pwd)
    print("Your user ID is :- ", uid)
    users.update({u.uid: u})

    # Save users to CSV
    save_users_to_csv()

    menu()


def login(flag=''):
    global uid
    global pwd
    uid = acceptors.accept_uid()
    pwd = acceptors.accept_pwd()
    if uid in users and users[uid].pwd == pwd:
        print("\nWelcome ", users[uid].name, " !\n")
        global logged_in
        logged_in = True
    else:
        print("\nNo such user ID / Wrong Password !\n")
        return login()
    if flag == '':
        menu()
    else:
        pass


def check_prev_bookings():
    if not logged_in:
        login('p')
    for i in users[uid].history:
        print("\nPNR number = ", i)
        check_pnr(i)
    menu()


def end():
    s()
    print("-"*24,"Thank You","-"*24)
    print("-"*59)
    sys.exit()


t1 = train('odisha', 12345, '12:34', '22:12', 'ctc', 'kgp', 'Wed', 30, 23, 43, 2205, 320, 234)
t2 = train('howrah', 12565, '02:34', '23:12', 'hwr', 'kol', 'Mon', 33, 4, 12, 3434, 435, 234)
t3 = train('bangalore', 22353, '11:56', '03:12', 'ctc', 'ban', 'Fri', 33, 24, 77, 455, 325, 533)
t4 = train('visakhapatnam', 22364, '07:00', '10:00', 'vsk', 'mas', 'Fri', 33, 24, 77, 455, 325, 475)
trains = {t1.num: t1, t2.num: t2, t3.num: t3, t4.num: t4}
u1 = user(1111, 'kiran', 'cuttack', '7478021777', 'kiran')
u2 = user(2322, 'alex parrish', 'new york', '7873752967', 'alexparrish')
u3 = user(8576, 'Vinay', 'Visakhapatnam', '9999999999', 'swaroop')
users = {u1.uid: u1, u2.uid: u2, u3.uid: u3}
ticket_dict = {}

def load():
    global trains, users, ticket_dict
    trains = {}
    users = {}
    ticket_dict = {}

    # Load trains
    try:
        with open("trains.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                trains[int(row['num'])] = train(
                    name=row['name'],
                    num=int(row['num']),
                    arr_time=row['arr_time'],
                    dep_time=row['dep_time'],
                    src=row['src'],
                    des=row['des'],
                    day_of_travel=row['day_of_travel'],
                    seat_available_in_1AC=int(row['seat_available_in_1AC']),
                    seat_available_in_2AC=int(row['seat_available_in_2AC']),
                    seat_available_in_SL=int(row['seat_available_in_SL']),
                    fare_1ac=int(row['fare_1ac']),
                    fare_2ac=int(row['fare_2ac']),
                    fare_sl=int(row['fare_sl'])
                )
    except FileNotFoundError:
        print("No train data found. Starting fresh.")

    # Load users
    try:
        with open("users.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                users[int(row['uid'])] = user(
                    uid=int(row['uid']),
                    name=row['name'],
                    hometown=row['hometown'],
                    cell_num=row['cell_num'],
                    pwd=row['pwd']
                )
    except FileNotFoundError:
        print("No user data found. Starting fresh.")

    # Load tickets
    try:
        with open("tickets.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ticket_dict[row['pnr']] = ticket(
                    train=trains[int(row['train_num'])],
                    user=users[int(row['uid'])],
                    ticket_num=int(row['ticket_num']),
                    coach=row['coach']
                )
    except FileNotFoundError:
        print("No ticket data found. Starting fresh.")



def s():
    # Save trains
    with open("trains.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            'name', 'num', 'arr_time', 'dep_time', 'src', 'des', 'day_of_travel',
            'seat_available_in_1AC', 'seat_available_in_2AC', 'seat_available_in_SL',
            'fare_1ac', 'fare_2ac', 'fare_sl'
        ])
        writer.writeheader()
        for train_obj in trains.values():
            writer.writerow({
                'name': train_obj.name,
                'num': train_obj.num,
                'arr_time': train_obj.arr_time,
                'dep_time': train_obj.dep_time,
                'src': train_obj.src,
                'des': train_obj.des,
                'day_of_travel': train_obj.day_of_travel,
                'seat_available_in_1AC': train_obj.seats['1AC'],
                'seat_available_in_2AC': train_obj.seats['2AC'],
                'seat_available_in_SL': train_obj.seats['SL'],
                'fare_1ac': train_obj.fare['1AC'],
                'fare_2ac': train_obj.fare['2AC'],
                'fare_sl': train_obj.fare['SL']
            })

    # Save users
    with open("users.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=['uid', 'name', 'hometown', 'cell_num', 'pwd'])
        writer.writeheader()
        for user_obj in users.values():
            writer.writerow({
                'uid': user_obj.uid,
                'name': user_obj.name,
                'hometown': user_obj.hometown,
                'cell_num': user_obj.cell_num,
                'pwd': user_obj.pwd
            })

    # Save tickets
    with open("tickets.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=['pnr', 'train_num', 'coach', 'uid', 'ticket_num'])
        writer.writeheader()
        for pnr, ticket_obj in ticket_dict.items():
            writer.writerow({
                'pnr': pnr,
                'train_num': ticket_obj.train_num,
                'coach': ticket_obj.coach,
                'uid': ticket_obj.uid,
                'ticket_num': ticket_obj.ticket_num
            })



print("-"*10,"Welcome to Railway Reservation Portal","-"*10)
print("-"*59)
load()


def menu():
    print("Choose one of the following option:-")
    print("1.Book Ticket")
    print("2.Cancel Ticket")
    print("3.Check PNR ")
    print("4.Check seat availibity")
    print("5.Create new account")
    print("6.Check previous bookings")
    print("7.Login")
    print("8.Exit")
    func = {1: book_ticket, 2: cancel_ticket, 3: check_pnr, 4: check_seat_availabilty, 5: create_new_acc,
            6: check_prev_bookings, 7: login, 8: end}
    option = acceptors.accept_menu_option()
    
    # Save ticket data before executing the selected option
    save_tickets_to_csv()
    func[option]()


menu()
