cmake_minimum_required(VERSION 2.8)
project(opencv_cpp_tutorials)

#set(OpenCV_DIR /home/fzeng/opencv-3.1.0/build/) # Added this for home laptop
#set(OpenCV_LIBS /home/fzeng/opencv-3.1.0/build/lib) # Added this to set ${OpenCV_LIBS}
set(OpenCV_DIR /usr/local/share/OpenCV/)
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})


# add_subdirectory(src/Introduction_to_OpenCV/Load_and_Display_an_Image)
# add_subdirectory(src/Introduction_to_OpenCV/Load_and_Display_a_Video)
# add_subdirectory(src/The_Core_Functionality/Mat_The_Basic_Image_Container)
# add_subdirectory(src/The_Core_Functionality/How_to_Scan_Images)
# add_subdirectory(src/The_Core_Functionality/Operations_with_Images)
# add_subdirectory(src/The_Core_Functionality/Mask_Operations_on_Matrices)
# add_subdirectory(src/The_Core_Functionality/Contrast_and_Brightness)
# add_subdirectory(src/The_Core_Functionality/Basic_Drawing)
# add_subdirectory(src/The_Core_Functionality/Random_and_Text)
add_subdirectory(src/The_Core_Functionality/Discrete_Fourier_Transform)

