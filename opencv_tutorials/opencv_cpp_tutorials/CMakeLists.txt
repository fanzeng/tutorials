cmake_minimum_required(VERSION 2.8)
project(opencv_cpp_tutorials)

set(OpenCV_DIR /home/fzeng/opencv-3.1.0/build/) # Added this for home laptop

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})



# add_subdirectory(src/Introduction_to_OpenCV/Load_and_Display_an_Image)
#add_subdirectory(src/The_Core_Functionality/Mat_The_Basic_Image_Container)
add_subdirectory(src/The_Core_Functionality/How_to_Scan_Images)

