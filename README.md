# pitemp

This small file logs the temperature of a Raspberry pi and sends it to an Azure Event Hub. Event hub name and connection string are read from a JSON file.

It is ran by a cron script:
```
*/5 * * * * /home/pi/pitemp/pitemp/bin/python /home/pi/pitemp/pitemp/temp_sender.py  > /home/pi/pitemp/pitemp.log 2>&1
```
