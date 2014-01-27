import ThreadedTCPServer
import MyTCPHandlerJson
import Configuration
import socket
import drivers.X10ControllerAdapter

if __name__ == "__main__":
  # Load the configuration file
  #Configuration.Configuration()
  Configuration.Configuration.LoadConfiguration()
  
  print "X10 controller:", Configuration.Configuration.X10ControllerDevice()
  print "ComPort:", Configuration.Configuration.ComPort()
  
  # Inject the X10 controller driver
  driver = Configuration.Configuration.GetX10ControllerDriver()
  drivers.X10ControllerAdapter.X10ControllerAdapter.Open(driver)
  
  #HOST, PORT = "localhost", 9999
  #HOST, PORT = "hedwig", 9999
  # We'll use the current host name
  # TODO Work on this to use 0.0.0.0 as the host (accept from any interface)
  #HOST, PORT = socket.gethostbyname(socket.gethostname()), Configuration.Configuration.Port()
  # This accepts connections from any network interface. It was the only
  # way to get it to work in the RPi from remote machines.
  HOST, PORT = "0.0.0.0", Configuration.Configuration.Port()

  # Create the server, binding to localhost on port 9999
  #server = SocketServer.TCPServer((HOST, PORT), MyTCPHandlerStream)
  ThreadedTCPServer.ThreadedTCPServer.allow_reuse_address = True
  server = ThreadedTCPServer.ThreadedTCPServer((HOST, PORT), MyTCPHandlerJson.MyTCPHandlerJson)

  # Activate the server; this will keep running until you
  # interrupt the program with Ctrl-C
  print "AtHomePowerlineServer now serving sockets at {0}:{1}...".format(HOST, PORT)
  
  try:
    print "Use ctrl-c to shutdown server"
    server.serve_forever()
  except KeyboardInterrupt:
    print "\n"
    print "AtHomePowerlineServer shutting down..."
  except Exception as e: 
    print "Unhandled exception occurred\n"
    print e.strerror
    print sys.exc_info()[0]
  finally:
    server.shutdown()
    drivers.X10ControllerAdapter.X10ControllerAdapter.Close()
    print "AtHomePowerlineServer shutdown complete"