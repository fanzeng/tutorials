add_executable(OperationsWithImages.exe OperationsWithImages.cpp)
target_link_libraries(OperationsWithImages.exe ${OpenCV_LIBS})
set_target_properties(OperationsWithImages.exe
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
