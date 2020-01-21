add_executable(RandomAndText RandomAndText.cpp)
target_link_libraries(RandomAndText ${OpenCV_LIBS})
set_target_properties(RandomAndText
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
