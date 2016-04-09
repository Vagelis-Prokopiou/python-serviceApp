# ServiceApp
A Python application, to help you manage the periodic maintenance of your vehicle.

## Instructions
The main application is the "service.py" file. You just have to run it in your terminal. Use Python 3.

When you run it, the program asks for the current mileage of your vehicle. You have to provide this value. Then, the program checks if you have exceeded the allowed time or the allowed kilometres for every spare part of your vehicle, and informs you accordingly.

This file draws the data for the application from the "data.cvs" file, located within the same folder.

#### The "data.cvs" file

 This file contains 5 columns of data (separated with commas).

 - The "**element**". That is, the name of the spare part.
 - The "**dateChanged**". The date that the spare part was last changed. This has to be manually updated for the time being. Use the d/m/y format (e.g. 25/4/2015).
 - The "**dateInterval**". That is, the max time allowed by the manufacturer, for the specific spare part.
 - The "**kmsChanged**". That is, the kilometres (or miles) of the vehicle when this spare part was changed. This has to be manually updated for the time being.
 - The "**kmsInterval**". That is, the max kilometers allowed by the manufacturer, for the specific spare part.

Obviously, you have to update the aforementioned information, according to your vehicle specs.

## Roadmap
Automate some stuff, like the updating of the "**dateChanged**" and the "**kmsChanged**" fields of the "data.csv" file.

Enjoy.


