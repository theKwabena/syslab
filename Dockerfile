# Use the Alpine base image
FROM alpine:latest

# Install bash (optional, as Alpine uses ash by default)
RUN apk add --no-cache bash

# Set the working directory
WORKDIR /home

# Use bash as the default shell (optional)
SHELL ["/bin/bash", "-c"]

# Default command (can be overridden)
CMD ["bash"]
