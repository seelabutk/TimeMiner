#!/bin/bash

for i in {1..11}; do
	./get_views.py $i &
done
