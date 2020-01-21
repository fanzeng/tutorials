add_executable(DisplayVideo DisplayVideo.cpp)
target_link_libraries(DisplayVideo ${OpenCV_LIBS})
set_target_properties(DisplayVideo
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
