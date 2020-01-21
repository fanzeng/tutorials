add_executable(HowToScanImages HowToScanImages.cpp)
target_link_libraries(HowToScanImages ${OpenCV_LIBS})
set_target_properties(HowToScanImages
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
