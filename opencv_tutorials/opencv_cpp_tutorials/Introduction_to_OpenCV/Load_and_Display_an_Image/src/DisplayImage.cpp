#include <opencv2/core/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui/highgui.hpp>

#include <iostream>
#include <string>
using namespace std;
using namespace cv;

int main(int argc, char** argv)
{
    string imageName("../../../samples/HappyFish.jpg"); // default image;
    if (argc > 1)
    {
        imageName = argv[1];
    }

    Mat image;
}
