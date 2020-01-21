add_executable(FeatureMatchingWithFLANN FeatureMatchingWithFLANN.cpp)
target_link_libraries(FeatureMatchingWithFLANN ${OpenCV_LIBS})
set_target_properties(FeatureMatchingWithFLANN
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
