add_executable(DisplayImage.exe DisplayImage.cpp)
target_link_libraries(DisplayImage.exe ${OpenCV_LIBS})
set_target_properties(DisplayImage.exe
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
