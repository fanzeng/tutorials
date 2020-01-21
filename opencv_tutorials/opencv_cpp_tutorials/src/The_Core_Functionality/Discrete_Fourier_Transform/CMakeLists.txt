add_executable(DiscreteFourierTransform DiscreteFourierTransform.cpp)
target_link_libraries(DiscreteFourierTransform ${OpenCV_LIBS})
set_target_properties(DiscreteFourierTransform
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
