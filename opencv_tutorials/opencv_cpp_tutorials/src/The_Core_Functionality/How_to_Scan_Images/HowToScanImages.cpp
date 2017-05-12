#include <opencv2/opencv.hpp>
using namespace std;

cv::Mat& ScanImageAndReduceC(cv::Mat& I, const uchar* table);
cv::Mat& ScanImageAndReduceIterator(cv::Mat& I, const uchar* table);
cv::Mat& ScanImageAndReduceRandomAccess(cv::Mat& I, const uchar * table);


int main(int argc, char** argv)
{
    int divideWith = 0; //convert our input string to number - C++ style
    stringstream s;
    s << argv[2];
    s >> divideWith;
    if (!s || !divideWith)
    {
        cout << "Invalid number entered for dividing." << endl;
        return -1;
    }
    
    // Read in the image I
    cv::Mat I, J;
    if( argc == 4 && !strcmp(argv[3],"G") )
        I = cv::imread(argv[1], cv::IMREAD_GRAYSCALE);
    else
        I = cv::imread(argv[1], cv::IMREAD_COLOR);

    if (I.empty())
    {
        cout << "The image" << argv[1] << " could not be loaded." << endl;
        return -1;
    }else{
//        cv::namedWindow("original");
//        cv::imshow("original", I);
//        cv::waitKey(0);
//        cv::destroyAllWindows();
    }

    uchar table[256];
    for (int i = 0; i <256; ++i)
        table[i] = (uchar)(divideWith * (i/divideWith));
    cout << table;
   
    const int times = 100;
    double t;

    t = (double)cv::getTickCount();

    for (int i = 0; i < times; ++i)
    {
        cv::Mat clone_i = I.clone();
        J = ScanImageAndReduceC(clone_i, table);
    }

    t = 1000*((double)cv::getTickCount() - t) / cv::getTickFrequency();
    t /= times;

    cout << "Time of reducing with the C operator [] (averaged for "
         << times << " runs): " << t << " milliseconds."<< endl;

    t = (double)cv::getTickCount();
    

    for (int i = 0; i < times; ++i)
    {
        cv::Mat clone_i = I.clone();
        J = ScanImageAndReduceIterator(clone_i, table);
    }

    t = 1000*((double)cv::getTickCount() - t) / cv::getTickFrequency();
    t /= times;

    cout << "Time of reducing with the iterator (averaged for "
        << times << " runs): " << t << " milliseconds."<< endl;

    t = (double)cv::getTickCount();

    for (int i = 0; i < times; ++i)
    {
        cv::Mat clone_i = I.clone();
        ScanImageAndReduceRandomAccess(clone_i, table);
    }

    t = 1000*((double)cv::getTickCount() - t) / cv::getTickFrequency();
    t /= times;

    cout << "Time of reducing with the on-the-fly address generation - at function (averaged for "
        << times << " runs): " << t << " milliseconds."<< endl;

    //! [table-init]
    cv::Mat lookUpTable(1, 256, CV_8U);
    uchar* p = lookUpTable.ptr();
    for(int i = 0; i < 256; ++i)
        p[i] = table[i];
    //! [table-init]

    t = (double)cv::getTickCount();

    for (int i = 0; i < times; ++i)
        //! [table-use]
        cv::LUT(I, lookUpTable, J); // Look-up table
        //! [table-use]

    t = 1000*((double)cv::getTickCount() - t)/cv::getTickFrequency();
    t /= times;

    cout << "Time of reducing with the LUT function (averaged for "
        << times << " runs): " << t << " milliseconds."<< endl;
    cv::imwrite("./reduced.jpg", J);
    return 0;
}

  
// The most efficient method
cv::Mat& ScanImageAndReduceC(cv::Mat& I, const uchar* const table)
{
    // accept only char type matrices
    CV_Assert(I.depth() == CV_8U);

    int channels = I.channels();

    int nRows = I.rows;
    int nCols = I.cols * channels;

    if (I.isContinuous())
    {
        nCols *= nRows;
        nRows = 1;
    }

    
    int i,j;
    uchar* p;
    for(i = 0; i < nRows; ++i)
    {
        p = I.ptr<uchar>(i); // p is the pointer to the i'th row in the matrix I
        for (j = 0; j < nCols; ++j)
        {
            p[j] = table[p[j]];
        }
    }
    return I;
    
}

// The iterator (safe) method
cv::Mat& ScanImageAndReduceIterator(cv::Mat& I, const uchar* const table)
{
    // accept only char type matrices
    CV_Assert(I.depth() == CV_8U);

    const int channels = I.channels();
    switch(channels)
    {
    case 1:
        {
            cv::MatIterator_<uchar> it, end;
            for(it = I.begin<uchar>(), end = I.end<uchar>(); it != end; ++it)
                *it = table[*it];
            break;
        }
    case 3:
        {
            cv::MatIterator_<cv::Vec3b> it, end;
            for( it = I.begin<cv::Vec3b>(), end = I.end<cv::Vec3b>(); it != end; ++it)
            {
                (*it)[0] = table[(*it)[0]];
                (*it)[1] = table[(*it)[1]];
                (*it)[2] = table[(*it)[2]];
            }
        }
    }

    return I;
}

// On-the-fly address calculation with reference returning
cv::Mat& ScanImageAndReduceRandomAccess(cv::Mat& I, const uchar* const table)
{
    // accept only char type matrices
    CV_Assert(I.depth() == CV_8U);

    const int channels = I.channels();
    switch(channels)
    {
    case 1:
        {
            for(int i = 0; i < I.rows; ++i)
                for(int j = 0; j < I.cols; ++j)
                    I.at<uchar>(i,j) = table[I.at<uchar>(i,j)];
            break;
        }
    case 3:
        {
         cv::Mat_<cv::Vec3b> _I = I;

         for(int i = 0; i < I.rows; ++i)
            for(int j = 0; j < I.cols; ++j )
               {
                   _I(i,j)[0] = table[_I(i,j)[0]];
                   _I(i,j)[1] = table[_I(i,j)[1]];
                   _I(i,j)[2] = table[_I(i,j)[2]];
            }
         I = _I;
         break;
        }
    }

    return I;
}