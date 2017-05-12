#include <opencv2/opencv.hpp>
using namespace std;

int main(int argc, char** argv)
{
//   cv::Mat M(2,2, CV_8UC3, cv::Scalar(0,0,255));
    
   int sz[3] = {2, 2, 2};
   cv::Mat M(3, sz, CV_8UC(1), cv::Scalar::all(0)); // Cannot cout more than 2 dimension Mat

   M.create(4, 4, CV_8UC(2));
   cout << "M = " << endl << " " << M << endl << endl;
   
   cv::Mat E = cv::Mat::eye(4, 4, CV_64F);
   cout << "E=" << endl << " " << E << endl << endl;
   cv::Mat O = cv::Mat::ones(2, 2, CV_32F);
   cout << "O=" << endl << " " << O << endl << endl;
   cv::Mat Z = cv::Mat::zeros(3, 3, CV_8UC1);
   cout << "Z=" << endl << " " << Z << endl << endl;
   
   cv::Mat C = (cv::Mat_<double>(3, 3)<< 0, -1, 0, -1, 5, -1, 0, -1, 0);
   cout << "C=" << endl << " " << C << endl << endl;
   
   cv:: Mat RowClone = C.row(1).clone();
   cout << "RowClone=" << endl << " " << RowClone << endl << endl;
   
   cv::Mat R = cv::Mat(3, 2, CV_8UC3, cv::Scalar(5, 6, 7));
   cv::randu(R, cv::Scalar::all(0), cv::Scalar::all(25));
   cout << "R=" << endl << " " << R << endl << endl;
   cout << "R (default)=" << endl << R << endl << endl;
   cout << "R (python)=" << endl << format(R, cv::Formatter::FMT_PYTHON) << endl << endl;
   cout << "R (csv)=" << endl << format(R, cv::Formatter::FMT_CSV) << endl << endl;
   cout << "R (numpy)=" << endl << format(R, cv::Formatter::FMT_NUMPY) << endl << endl;
   cout << "R (c)=" << endl << format(R, cv::Formatter::FMT_C) << endl << endl;
   
   cv::Point2f P(5, 1);
   cout << "Point (2D)=" << P << endl << endl;
   
   cv::Point3f P3f(2, 6, 7);
   cout << "Point (3D=)" << P3f << endl << endl;
   
   vector<float> v;
   v.push_back((float)CV_PI); v.push_back(2); v.push_back(3.01f);
   cout << "Vector of floats via Mat =" << cv::Mat(v) << endl << endl;
   
   vector<cv::Point2f> vPoints(20);
   for (size_t i = 0; i < vPoints.size(); ++i)
   {
       vPoints[i] = cv::Point2f((float)(i * 5), (float)(i % 7));
   }
   cout << "A vector of 2D points = " << vPoints << endl << endl;
}

