add_executable(FeatureMatchingWithFLANN.exe FeatureMatchingWithFLANN.cpp)
target_link_libraries(FeatureMatchingWithFLANN.exe ${OpenCV_LIBS})
set_target_properties(FeatureMatchingWithFLANN.exe
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
