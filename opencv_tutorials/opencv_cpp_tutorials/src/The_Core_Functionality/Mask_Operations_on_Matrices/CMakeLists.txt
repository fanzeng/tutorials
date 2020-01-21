add_executable(MaskOperationsOnMatrices MaskOperationsOnMatrices.cpp)
target_link_libraries(MaskOperationsOnMatrices ${OpenCV_LIBS})
set_target_properties(MaskOperationsOnMatrices
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
