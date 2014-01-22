import ThreadedTCPServer
import MyTCPHandlerJson
import socket
import drivers.X10ControllerAdapter
#import drivers.X10ControllerInterface
import drivers.XTB232

if __name__ == "__main__":
  # Inject the X10 controller driver
  drivers.X10ControllerAdapter.X10ControllerAdapter().InjectDriver(drivers.XTB232.XTB232())
  
  #HOST, PORT = "localhost", 9999
  #HOST, PORT = "hedwig", 9999
  # We'll use the current host name
  HOST, PORT = socket.gethostname(), 9999

  # Create the server, binding to localhost on port 9999
  #server = SocketServer.TCPServer((HOST, PORT), MyTCPHandlerStream)
  ThreadedTCPServer.ThreadedTCPServer.allow_reuse_address = True
  server = ThreadedTCPServer.ThreadedTCPServer((HOST, PORT), MyTCPHandlerJson.MyTCPHandlerJson)

  # Activate the server; this will keep running until you
  # interrupt the program with Ctrl-C
  print "AtHomePowerlineServer now serving sockets at {0}:{1}...".format(HOST, PORT)
  
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    print "\n"
    print "AtHomePowerlineServer shutting down..."
  except Exception as e: 
    print "Unhandled exection occurred\n"
    print e.strerror
    print sys.exc_info()[0]
  finally:
    server.shutdown()
    print "AtHomePowerlineServer shutdown complete"