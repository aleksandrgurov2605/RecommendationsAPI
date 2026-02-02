#!/bin/bash
export PYTHONPATH=/home/rec_shop
python /home/rec_shop/seed.py

# docker exec -it recs-web-1 /home/rec_shop/seed.sh