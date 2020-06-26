# JH Software Developer Interview Assignment

## INTRO

This challenge has been attempted in accordance with the guidelines provided [here](/Guidelines.pdf)

## Dependencies
1. Python 3.8.2
2. Pipenv

## RUN

1. Ensure your JSON data is put inside the folder `/inputs`
2. While at the root folder run  `pipenv shell` to activate virtual environment.
3. To run the script use `python main.py`

The results will be processed and stored inside the `/outputs` folder in a `results.csv` file.

Logs are mantainede in the `process.log` file.

## Assumptions Made
1. All `user_id`s from the json files have to be valid. For a user Id to be valid it must be a member of this set:
{ 43019547057,43050067402,43050067304,43050067221,43050067495,43049279159, 43068095002,43038614851,43067338910,43019546306,43050067351}
2. The `created_at` field denotes order in which the messages were send so a later tiem indicates that the message was send later.


## Authors
- [Joseph Mutuku Kyalo](https://github.com/thoth-ky)
