cmake_minimum_required(VERSION 2.8)
project(opencv_cpp_tutorials)

find_package(OpenCV REQUIRED)
if(OpenCV_FOUND)
   message("Found OpenCV")
   message("OpenCV_INCLUDE_DIRS=" ${OpenCV_INCLUDE_DIRS})
   message("OpenCV_DIR=" ${OpenCV_DIR})
endif(OpenCV_FOUND)

include_directories(${OpenCV_INCLUDE_DIRS})

add_subdirectory(Introduction_to_OpenCV)
add_subdirectory(The_Core_Functionality)
add_subdirectory(2D_Features_Framework)
