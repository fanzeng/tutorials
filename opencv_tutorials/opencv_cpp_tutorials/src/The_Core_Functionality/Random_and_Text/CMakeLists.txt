add_executable(RandomAndText.exe RandomAndText.cpp)
target_link_libraries(RandomAndText.exe ${OpenCV_LIBS})
set_target_properties(RandomAndText.exe
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
