from data_manager import DataManager
from datetime import datetime, timedelta
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIGIN_CITY_IATA_CODE = 'LON'

flight_search = FlightSearch()
notification_manager = NotificationManager()
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()

for item in sheet_data:
    if item['iataCode'] == '':
        item['iataCode'] = flight_search.get_destinatation_code(item['city'])
        data_manager.destination_data = sheet_data
        data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_months_from_now = datetime.now() + timedelta(days=(30 * 6))

for destination in sheet_data:
    flight = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_IATA_CODE,
        destination_city_code=destination['iataCode'],
        from_time=tomorrow,
        to_time=six_months_from_now
    )

    # If no flight within 6 months, terminate this iteration (skip remaining statements in 'for' block) and move onto
    # next destination.

    if flight is None:
        continue

    if flight.price < destination['lowestPrice']:
        user_data = data_manager.get_customer_data()
        emails = [user['email'] for user in user_data]
        booking_link = flight.booking_link

        message = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport}" \
                  f" to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} " \
                  f"to {flight.return_date}. "

        notification_manager.send_emails(emails=emails, email_message_body=message, google_flight_link=booking_link)
        notification_manager.send_text(message)
