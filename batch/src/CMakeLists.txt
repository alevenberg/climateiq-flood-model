add_executable(main main.cc)

target_link_libraries("main" PRIVATE google-cloud-cpp::batch)