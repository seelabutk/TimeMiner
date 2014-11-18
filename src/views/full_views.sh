#!/bin/bash

for i in {1..3}; do
	./get_views.py $i &
done
