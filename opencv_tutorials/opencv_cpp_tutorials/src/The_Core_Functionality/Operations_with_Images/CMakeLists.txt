add_executable(OperationsWithImages OperationsWithImages.cpp)
target_link_libraries(OperationsWithImages ${OpenCV_LIBS})
set_target_properties(OperationsWithImages
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
