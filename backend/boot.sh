#!/bin/bash

# Boot script for Railway deployment with OpenCV
# Creates symlinks for shared libraries that OpenCV needs

echo "Setting up library symlinks for OpenCV..."

# Create lib directory if it doesn't exist
mkdir -p /usr/lib

# Find and symlink libGL
if [ ! -f /usr/lib/libGL.so.1 ]; then
    LIBGL=$(find /nix/store -name "libGL.so.1" 2>/dev/null | head -n 1)
    if [ -n "$LIBGL" ]; then
        ln -sf "$LIBGL" /usr/lib/libGL.so.1
        echo "Linked libGL.so.1"
    fi
fi

# Find and symlink glib
if [ ! -f /usr/lib/libglib-2.0.so.0 ]; then
    LIBGLIB=$(find /nix/store -name "libglib-2.0.so.0" 2>/dev/null | head -n 1)
    if [ -n "$LIBGLIB" ]; then
        ln -sf "$LIBGLIB" /usr/lib/libglib-2.0.so.0
        echo "Linked libglib-2.0.so.0"
    fi
fi

# Find and symlink gthread
if [ ! -f /usr/lib/libgthread-2.0.so.0 ]; then
    LIBGTHREAD=$(find /nix/store -name "libgthread-2.0.so.0" 2>/dev/null | head -n 1)
    if [ -n "$LIBGTHREAD" ]; then
        ln -sf "$LIBGTHREAD" /usr/lib/libgthread-2.0.so.0
        echo "Linked libgthread-2.0.so.0"
    fi
fi

# Find and symlink libSM
if [ ! -f /usr/lib/libSM.so.6 ]; then
    LIBSM=$(find /nix/store -name "libSM.so.6" 2>/dev/null | head -n 1)
    if [ -n "$LIBSM" ]; then
        ln -sf "$LIBSM" /usr/lib/libSM.so.6
        echo "Linked libSM.so.6"
    fi
fi

echo "Library setup complete. Starting application..."

# Start the FastAPI application
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
