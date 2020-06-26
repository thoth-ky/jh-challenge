import logging
from app.process import load_input_files, fix_time_delta, persist_output_csv

def main():
  conversations = load_input_files('inputs')
  final_data = fix_time_delta(conversations)
  persist_output_csv(final_data, 'outputs/results.csv')

if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s -> %(levelname)s:%(message)s',
    filename='process.log',
    filemode='w',
    level=logging.DEBUG)
  main()
    