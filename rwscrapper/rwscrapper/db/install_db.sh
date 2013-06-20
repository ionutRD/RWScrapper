#!/bin/bash

mysql -u root -p < pre.sql
mysql -u scrapper -p -e "create database DEX character set utf8"
mysql -u scrapper -p DEX < dex-database.sql
