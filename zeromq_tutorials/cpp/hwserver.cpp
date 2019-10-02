#include <zmq.hpp>
#include <string>
#include <iostream>
#ifndef _WIN32
#include <unistd.h>
#else
#include <windows.h>
#define sleep(n) Sleep(n)
#endif


int main() {
    zmq::context_t context(1);
    zmq::socket_t socket(context, ZMQ_REP);
    socket.bind("tcp://127.0.0.1:5555");

    while(true) {
        zmq::message_t request;
        socket.recv(&request);
        std::cout << "Received Hello" << std::endl;
        sleep(1);

        zmq::message_t reply(5);
        memcpy(reply.data(), "World", 5);
        socket.send(reply);
    }
    return 0;
}
