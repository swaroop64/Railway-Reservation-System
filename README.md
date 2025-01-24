# Railway Reservation System

This project is a console-based Railway Reservation System implemented in Python. It allows users to book and cancel train tickets, check seat availability, create new accounts, and view past bookings.

## Features

1. **Book Tickets**: Users can book tickets for trains based on seat availability and pay the fare.
2. **Cancel Tickets**: Users can cancel previously booked tickets, and the seats will be made available again.
3. **Check PNR**: Users can check their booking details using the PNR number.
4. **Check Seat Availability**: Users can see the available seats in different coaches (1AC, 2AC, SL) for specific trains.
5. **Create New Account**: New users can create an account to use the system.
6. **Login**: Existing users can log in to book or cancel tickets.
7. **View Previous Bookings**: Logged-in users can view their booking history.
8. **Persistent Data Storage**: Train, user, and ticket information is saved to CSV files and reloaded when the program restarts.

## Prerequisites

- Python 3.x
- A terminal or console to run the script


## File Structure

- `railway_reservation.py`: The main Python script for the Railway Reservation System.
- `trains.csv`: Stores train details (created or updated automatically by the program).
- `users.csv`: Stores user account details (created or updated automatically by the program).
- `tickets.csv`: Stores ticket booking details (created or updated automatically by the program).

## How It Works

### Booking Tickets
- Users can select a train, coach type (1AC, 2AC, SL), and the number of tickets to book.
- The system checks for availability and calculates the fare before confirming the booking.

### Cancelling Tickets
- Users can cancel their tickets by providing the PNR number.
- The system updates the seat availability and removes the ticket from the user's history.

### Persistent Data
- Train, user, and ticket information is saved to CSV files (`trains.csv`, `users.csv`, `tickets.csv`) to ensure data persistence.
- The data is loaded automatically when the program starts.

## Example Commands

- **Book a Ticket**: Choose option `1` in the main menu.
- **Cancel a Ticket**: Choose option `2` and provide the PNR number.
- **Check PNR**: Choose option `3` and provide the PNR number.
- **Check Seat Availability**: Choose option `4` and enter the source and destination stations.
- **Create a New Account**: Choose option `5` and provide your details.
- **Login**: Choose option `7` and enter your user ID and password.

## Future Enhancements

- Implementing a graphical user interface (GUI) for better user experience.
- Adding payment gateway integration.
- Enhancing train scheduling and route management.
- Allowing advanced booking for multiple dates.

Feel free to fork and enhance this project. Contributions are welcome! 😊
