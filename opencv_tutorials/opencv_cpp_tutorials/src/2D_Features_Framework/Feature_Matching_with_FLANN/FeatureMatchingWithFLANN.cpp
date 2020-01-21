#include <stdio.h>
#include <iostream>
#include <opencv2/highgui.hpp>
#include "opencv2/core.hpp"
#include "opencv2/features2d.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/xfeatures2d.hpp"

using namespace std;

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cout << "usage: FeatureMatchingWithFLANN [path_to_image_0]"
                " [path_to_image_1] "<< std::endl;
    }

    cv::Mat img_1 = cv::imread(argv[1], cv::IMREAD_GRAYSCALE);
    cv::Mat img_2 = cv::imread(argv[2], cv::IMREAD_GRAYSCALE);
    if (!img_1.data || !img_2.data) {
        cout << "Error reading images." << endl;
        return -1;
    }
    int minHessian = 400;
    cv::Ptr<cv::xfeatures2d::SURF> detector = cv::xfeatures2d::SURF::create();
    detector->setHessianThreshold(minHessian);
    
    vector<cv::KeyPoint> keypoints_1, keypoints_2;
    cv::Mat descriptors_1, descriptors_2;
    
    detector->detectAndCompute(img_1, cv::Mat(), keypoints_1, descriptors_1);
    detector->detectAndCompute(img_2, cv::Mat(), keypoints_2, descriptors_2);
    
    cv::FlannBasedMatcher matcher;
    vector<cv::DMatch> matches;
    matcher.match(descriptors_1,descriptors_2, matches);
    
    double max_dist = 0, min_dist = 100;
    for (int i = 0; i < descriptors_1.rows; i++) {
        double dist = matches[i].distance;
        if (dist < min_dist) min_dist = dist;
        if (dist > max_dist) max_dist = dist;
    }
    cout << "max_dist = " << max_dist << endl;
    cout << "min_dist = " << min_dist << endl;
    
    vector<cv::DMatch> good_matches;
    for (int i = 0; i < descriptors_1.rows; i++) {
        if (matches[i].distance <= max(2*min_dist, 0.02)) {
            good_matches.push_back(matches[i]);
        }
    }
    cv::Mat img_matches;
    cv::drawMatches(img_1, keypoints_1, img_2, keypoints_2, good_matches, img_matches, cv::Scalar::all(-1), cv::Scalar::all(-1), vector<char>(), cv::DrawMatchesFlags::NOT_DRAW_SINGLE_POINTS);
    cv::imshow("Good Matches", img_matches);
    cv::waitKey(0);
    return 0;
    
}