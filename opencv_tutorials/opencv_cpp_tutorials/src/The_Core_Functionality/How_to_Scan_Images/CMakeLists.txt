add_executable(HowToScanImages.exe HowToScanImages.cpp)
target_link_libraries(HowToScanImages.exe ${OpenCV_LIBS})
set_target_properties(HowToScanImages.exe
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
