# ServiceApp
A Python application, to help you manage the periodic maintenance of your vehicle.

## Description of the app
When you run it, the program asks for the current mileage of your vehicle. You have to provide this value.

Then, the program asks if you made any servicing, and you want to update_entry the data. If so, provide the appropriate info. The program updates automatically the "data.csv" file.

Then, the program checks if you have exceeded the allowed time or the allowed kilometres for every spare part of your vehicle, and informs you accordingly.

This file draws the data for the application from the "data.cvs" file, located within the same folder.

### The "data.cvs" file

 This file contains 5 columns of data (separated with commas).

 - The "**element**". That is, the name of the spare part.
 - The "**dateChanged**". The date that the spare part was last changed. If you edit this, use the day/month/year format (e.g. 31/12/2015).
 - The "**dateInterval**". That is, the max time (in **months**) allowed by the manufacturer, for the specific spare part.
 - The "**kmsChanged**". That is, the kilometres (or miles) of the vehicle when this spare part was changed.
 - The "**kmsInterval**". That is, the max kilometers allowed by the manufacturer, for the specific spare part.

Obviously, you have to update the "data.cvs" information, according to your vehicle specs.

## Running the app
The main application is the "service.py" file.

Change directory ("cd") in the root folder and run:

```bash
python3 serviceApp.py
```

"python3" usually is a simlink to python3.4. So if "python3" doesn't work, use:

```bash
python3.4 serviceApp.py
```

If you are a Windows user, you can download Python from https://www.python.org/downloads, and run it with python (from within the root folder):

```bash
python serviceApp.py
```
Alternatively, you can use the Windows executable (see below).

## Instructions to run the Windows serviceApp.exe
- Open you windows terminal (Command Prompt) and change directory (cd) to the "dist/serviceApp" folder within the root folder of the app.

- Update the "data.csv" file within this folder according to your needs.

- You are ready to run the application. Type:

```bash
serviceApp.exe
```

___

Enjoy.


