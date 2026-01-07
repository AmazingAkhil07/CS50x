-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Find the crime scene report for the theft on Humphrey Street
SELECT *
FROM crime_scene_reports
WHERE date = '2025-07-28'
  AND street = 'Humphrey Street';

-- Look at interviews from the same day to gather clues from witnesses
SELECT *
FROM interviews
WHERE date = '2025-07-28';

-- Identify phone calls made on the day of the theft that were short
SELECT *
FROM phone_calls
WHERE date = '2025-07-28'
  AND duration < 60;

-- Identify ATM withdrawals made on the day of the theft near Humphrey Street
SELECT *
FROM atm_transactions
WHERE date = '2025-07-28'
  AND transaction_type = 'withdraw';

-- Find flights leaving Fiftyville the day after the theft
SELECT *
FROM flights
WHERE origin_airport_id = (
    SELECT id FROM airports WHERE city = 'Fiftyville'
)
AND day = 29
AND month = 7
AND year = 2025;

-- Find the earliest flight out of Fiftyville
SELECT *
FROM flights
WHERE origin_airport_id = (
    SELECT id FROM airports WHERE city = 'Fiftyville'
)
AND day = 29
AND month = 7
AND year = 2025
ORDER BY hour, minute
LIMIT 1;

-- Find passengers on that earliest flight
SELECT *
FROM passengers
WHERE flight_id = (
    SELECT id FROM flights
    WHERE origin_airport_id = (
        SELECT id FROM airports WHERE city = 'Fiftyville'
    )
    AND day = 29
    AND month = 7
    AND year = 2025
    ORDER BY hour, minute
    LIMIT 1
);

-- Match passengers to people to identify suspects
SELECT people.name
FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE passengers.flight_id = (
    SELECT id FROM flights
    WHERE origin_airport_id = (
        SELECT id FROM airports WHERE city = 'Fiftyville'
    )
    AND day = 29
    AND month = 7
    AND year = 2025
    ORDER BY hour, minute
    LIMIT 1
);

-- Narrow suspects using phone call data
SELECT people.name
FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE phone_calls.date = '2025-07-28'
  AND phone_calls.duration < 60;

-- Identify the accomplice based on who received the call
SELECT people.name
FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE phone_calls.date = '2025-07-28'
  AND phone_calls.duration < 60;

