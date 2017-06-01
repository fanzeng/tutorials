add_executable(BasicDrawing.exe BasicDrawing.cpp)
target_link_libraries(BasicDrawing.exe ${OpenCV_LIBS})
set_target_properties(BasicDrawing.exe
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
