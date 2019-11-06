#!/bin/bash

flask db upgrade
flask run --with-threads