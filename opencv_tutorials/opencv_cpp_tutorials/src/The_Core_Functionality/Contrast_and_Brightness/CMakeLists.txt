add_executable(ContrastAndBrightness.exe ContrastAndBrightness.cpp)
target_link_libraries(ContrastAndBrightness.exe ${OpenCV_LIBS})
set_target_properties(ContrastAndBrightness.exe
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
