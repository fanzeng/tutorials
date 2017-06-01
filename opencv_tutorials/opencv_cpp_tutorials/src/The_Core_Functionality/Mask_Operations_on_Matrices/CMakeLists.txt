add_executable(MaskOperationsOnMatrices.exe MaskOperationsOnMatrices.cpp)
target_link_libraries(MaskOperationsOnMatrices.exe ${OpenCV_LIBS})
set_target_properties(MaskOperationsOnMatrices.exe
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
