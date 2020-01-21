add_executable(ContrastAndBrightness ContrastAndBrightness.cpp)
target_link_libraries(ContrastAndBrightness ${OpenCV_LIBS})
set_target_properties(ContrastAndBrightness
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
