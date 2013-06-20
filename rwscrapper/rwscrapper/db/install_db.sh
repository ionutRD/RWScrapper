#!/bin/bash

mysql -u root -p < pre.sql
mysql -u scrapper -p DEX < dex-database.sql
