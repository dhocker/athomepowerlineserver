import SocketServer

"""
TCP server using threads.
Supports JSON formatted payloads.
"""
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
  pass
