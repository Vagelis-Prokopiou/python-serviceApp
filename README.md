# ServiceApp
A Python application, to help you manage the periodic maintenance of your vehicle.

## Instructions (to run the Python file)
The main application is the "service.py" file. You just have to run it in your terminal.

```bash
python3 service.py
```

Use Python 3. If you are a Windows user, you can download Python from https://www.python.org/downloads, or use the executable (see below). If you are a Linux user, I take for granted that you know how to use the program... :)

When you run it, the program asks for the current mileage of your vehicle. You have to provide this value. Then, the program checks if you have exceeded the allowed time or the allowed kilometres for every spare part of your vehicle, and informs you accordingly.

This file draws the data for the application from the "data.cvs" file, located within the same folder.

#### The "data.cvs" file

 This file contains 5 columns of data (separated with commas).

 - The "**element**". That is, the name of the spare part.
 - The "**dateChanged**". The date that the spare part was last changed. This has to be manually updated for the time being. Use the d/m/y format (e.g. 25/4/2015).
 - The "**dateInterval**". That is, the max time (in **months**) allowed by the manufacturer, for the specific spare part.
 - The "**kmsChanged**". That is, the kilometres (or miles) of the vehicle when this spare part was changed. This has to be manually updated for the time being.
 - The "**kmsInterval**". That is, the max kilometers allowed by the manufacturer, for the specific spare part.

Obviously, you have to update the aforementioned information, according to your vehicle specs.


## Instructions (to run the Windows .exe)
Open you windows terminal (Command Prompt) and change directory (cd) to the "service" folder within the root folder.

In there, there also is a "data.csv" file which you have to edit according to your needs.

After that, you are ready to run the application. Type

```bash
service.exe
```

and voila!


## Roadmap
Automate some stuff, like the updating of the "**dateChanged**" and the "**kmsChanged**" fields of the "data.csv" file.

___

Enjoy.


