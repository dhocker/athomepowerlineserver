import ServerCommand
import datetime

# Command handler for loading timer initiators
class LoadTimers(ServerCommand.ServerCommand):
  
  # Execute the load timers command.
  # We replace the current set of timer programs/initiators with
  # whatever is in the request payload.
  def Execute(self, request):    
    # The CM11A X10 controller expects time in terms of the number of minutes
    # since midnight of the current day. Here, we play with converting
    # the on/off times to that format.
    # Note: In this implementation there is not real reason to limit timers
    # to the HH:MM format. We are never going to store these in an X10 controller.
    # In this implementation the server IS the X10 controller. The hardware X10 controller
    # is just a down-stream component used to transmit immediate X10 signals.
    for timer_program in request["args"]:
      t = datetime.datetime.strptime(timer_program["ontime"], "%H:%M")
      #print "ontime:", timer_program["ontime"]
      print "ontime:", t, "minutes:", (t.hour * 60) + t.minute

    # TODO Update database with new programs.
    # TODO Put new timer programs into effect.
    
    # Generate a successful response
    response = LoadTimers.CreateResponse()
    r = response["X10Response"]
    
    r['command'] = "LoadTimers"
    r['resultcode'] = 0
    #r['error'] = "Command not implemented"
    r['datetime'] = str(datetime.datetime.now())
    r['message'] = "Success"

    return response