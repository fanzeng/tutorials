import zmq

context = zmq.Context()

print 'connecting to hello world server ...'
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')

for request in range(10):
    print 'sending request %s ...' % request
    socket.send(b'Hello')

    message = socket.recv()
    print 'received reply %s [ %s ] ' % (request, message)
