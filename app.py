import RPi.GPIO as GPIO
import time
from flask import Flask, render_template, request
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
    5 : {'name' : 'Change Speed', 'state' : GPIO.LOW},
    6 : {'name' : 'Faster/Slower', 'state' : GPIO.LOW},
    23 : {'name' : 'Motor Rotation', 'state' : GPIO.LOW},
    24 : {'name' : 'Motor Driver Enabled', 'state' : GPIO.HIGH}
}


# Set each pin as an output and initialize:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, pins[pin]['state'])

@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<command>/<action>")
def action(command, action):
    #print(command)
    if command == "enable":
        if action == "on":
            GPIO.output(24,GPIO.LOW)
        else:
            GPIO.output(24,GPIO.HIGH)

    if command == "rotation":
        if action == "CCW":
            GPIO.output(23,GPIO.HIGH)
        else:
            GPIO.output(23,GPIO.LOW)

    if command == "increase":
        GPIO.output(6,GPIO.HIGH)
        SpeedAction(action)

    if command == "decrease":
        GPIO.output(6,GPIO.LOW)
        SpeedAction(action)
    
   # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
    templateData = {
        'pins' : pins
    }

    return render_template('main.html', **templateData)

def SpeedAction(action):
    print(action)
    action = int(action)
    for x in range(action):
        GPIO.output(5,GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(5,GPIO.LOW)
        time.sleep(.1)
    return

'''
# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
   }

   return render_template('main.html', **templateData)
'''

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)