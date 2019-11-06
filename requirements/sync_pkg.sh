#!/bin/bash

# prod reqs
pip-compile -o requirements.txt requirements.in

# dev reqs
pip-compile -o requirements.dev.txt requirements.dev.in

# test reqs
pip-compile -o requirements.test.txt requirements.test.in

# move deps up
mv requirements.txt ..
mv requirements.dev.txt ..
mv requirements.test.txt ..