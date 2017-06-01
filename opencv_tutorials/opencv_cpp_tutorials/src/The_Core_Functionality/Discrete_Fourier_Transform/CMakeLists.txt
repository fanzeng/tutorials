add_executable(DiscreteFourierTransform.exe DiscreteFourierTransform.cpp)
target_link_libraries(DiscreteFourierTransform.exe ${OpenCV_LIBS})
set_target_properties(DiscreteFourierTransform.exe
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
