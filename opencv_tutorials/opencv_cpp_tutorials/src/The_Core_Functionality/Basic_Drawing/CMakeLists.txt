add_executable(BasicDrawing BasicDrawing.cpp)
target_link_libraries(BasicDrawing ${OpenCV_LIBS})
set_target_properties(BasicDrawing
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
