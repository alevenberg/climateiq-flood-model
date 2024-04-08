cmake_minimum_required(VERSION 3.20)

project(climateiq-gcp-batch CXX)

find_package(google_cloud_cpp_batch REQUIRED)

add_subdirectory(src)
