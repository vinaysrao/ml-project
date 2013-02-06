CC=g++
CFLAGS=-g `pkg-config --cflags --libs opencv`

surf:
	$(CC) -o $@ surf.cpp $(CFLAGS)