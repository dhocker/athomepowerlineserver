import ThreadedTCPServer
import MyTCPHandlerJson

if __name__ == "__main__":
  #HOST, PORT = "localhost", 9999
  HOST, PORT = "hedwig", 9999

  # Create the server, binding to localhost on port 9999
  #server = SocketServer.TCPServer((HOST, PORT), MyTCPHandlerStream)
  server = ThreadedTCPServer.ThreadedTCPServer((HOST, PORT), MyTCPHandlerJson.MyTCPHandlerJson)

  # Activate the server; this will keep running until you
  # interrupt the program with Ctrl-C
  print "Now serving sockets at {0}:{1}...".format(HOST, PORT)
  
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    print "\n"
    print "AtHomePowerlineServer shutting down..."
  except Exception as e: 
    print "Unhandled exection occurred\n"
    print e.strerrpr
    print sys.exc_info()[0]
  finally:
    server.shutdown()
    print "AtHomePowerlineServer shutdown complete"