#include <opencv2/opencv.hpp>
using namespace std;

int main(int argc, char** argv)
{
    int divideWith = 0; //convert our input string to number - C++ style
    stringstream s;
    s <<argv[2];
    s >> divideWith;
    if (!s || !divideWith)
    {
        cout << "Invalid number entered for deviding." << endl;
        return -1;
    }
    cout <<"H";
    uchar table[256];
    for (int i = 0; i <256; ++i)
        table[i] = (uchar)(divideWith * (i/divideWith));
    cout << table;
    return 0;
}

