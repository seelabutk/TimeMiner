#!/bin/bash

for i in {7..11}; do
	./get_views.py $i &
done
