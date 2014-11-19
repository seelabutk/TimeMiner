#!/bin/bash

for i in {4..6}; do
	./get_views.py $i &
done
