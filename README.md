# TicketMaster concert scraper by artist (Canada only)

Simple scraper with email alerts for new concerts, intended to be executed periodically (i.e., once a day).

### How does it work?

The scraper will send a request at the url *https://www.ticketmaster.ca/search?q=*, where the q will be the selected **artist in** ***main.py**.* Then, using the response obtained with this request, the script will extract all the **national events** from this artist which will be compared with the events saved in a sqlite database, If there are new events the script will send an **email alert** with the new events in the next format.

### How to use?

You will need a Gmail account with a app password to send the email alerts, otherwise, you will have to modify the *send_email* function to adjust it to the needs of your email provider.

1. Set the artist name in main.py
2. Create a *.env* file and set the next enviorement variables:
   1. *sender:* Email address to send the email alert
   2. *receiver:* Email address to receive the email alert
   3. *sender_pass:* Email password to login to the email sender address
3. Install the *requierements.txt* file.
4. Set the execution of the script in a task scheduler, this could be the Windows task scheduler, PythonAnywhere, or any service that meets your needs.
5. Execute the *main.py* file, the first time you will receive an email with the full list of events of that artist, and in the next executions you will receive only the new events published in ticketmaster.

*Note: You can also set the email variables manually on the *send_email* function and skip the *.env* file step.
