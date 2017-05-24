add_executable(DisplayVideo.exe DisplayVideo.cpp)
target_link_libraries(DisplayVideo.exe ${OpenCV_LIBS})
set_target_properties(DisplayVideo.exe
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
