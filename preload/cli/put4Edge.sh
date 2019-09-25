#!/bin/bash
for i in {1..4}
do
	python3 put_test.py edge-config-files/edge$(($i*2))_config.json str $((100*$(($i-1)) + 1)) 100 1mbfile 1 1 $i &
done
