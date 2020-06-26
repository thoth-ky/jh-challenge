import logging
from os import listdir, path
from json import load
from csv import DictWriter
from operator import itemgetter
from datetime import datetime
from collections import deque

# class to hold each message object
class Message:
  def __init__(self, ticket_number, user_id, entry_datetime):
    self.ticket_number = ticket_number
    self.entry_direction = self._set_entry_direction(user_id)
    self.entry_datetime = datetime.strptime(
      entry_datetime, "%Y-%m-%dT%H:%M:%SZ",
      )
    self.timedelta_hours = None
  
  def _set_entry_direction(self, user_id):
    # private setter method for message direction
    IN_USER_IDS = (43019547057,)
    OUT_USER_IDS = (
      43050067402,
      43050067304,
      43050067221,
      43050067495,
      43049279159,
      43068095002,
      43038614851,
      43067338910,
      43019546306,
      43050067351,
      )
    if user_id in IN_USER_IDS:
      return 'in'
    elif user_id in OUT_USER_IDS:
      return 'out'
    else:
      raise('Invalid User ID provided for message')

  def __repr__(self):
    return f'TN: {self.ticket_number} - {self.entry_direction}:\
      {self.entry_datetime.strftime("%Y-%m-%d %H:%M:%S")}'

  def to_dict(self):
    return {
      'ticket_number': self.ticket_number,
      'entry_direction': self.entry_direction,
      'entry_datetime': self.entry_datetime,
      'timedelta_hours': self.timedelta_hours
    }

def destructure (dictionary, *keys):
  # select specific keys from a dictionary
  return [ dictionary[key] if key in dictionary else None for key in keys ]

def load_json_file(path_to_json):
  result = []
  with open(path_to_json) as json_file:
    data = load(json_file)
    for message in data:
      [ticket_number, user_id, entry_datetime] = destructure(
        message, 'ticket_id', 'user_id', 'created_at'
        )
      result.append(Message(ticket_number, user_id, entry_datetime))
  # sort by date to arrange messages in order
  sorted_result = sorted(result, key=lambda k: k.entry_datetime)
  return sorted_result


def load_input_files(path_to_input_folder):
  logging.debug(f'Reading input files from {path_to_input_folder}')
  conversations = {}
  onlyfiles = [path.join(path_to_input_folder, f) for f in listdir(path_to_input_folder)\
    if path.isfile(path.join(path_to_input_folder, f))]
  
  for file_path in onlyfiles:
    logging.debug(f'Loading data from {file_path}')
    conversations.update({
      path.basename(file_path).split('.')[0]: load_json_file(file_path)
      })
  return conversations

def convert_timedelta_to_hours(timedelta):
  days = timedelta.days
  seconds = timedelta.seconds + (timedelta.microseconds / 1e6)
  return (days*24) + (seconds/3600)

def fix_time_delta(conversations):
  final_data = []
  for ticket_id, messages in conversations.items():
    set_in = False
    start_time = None

    for message in messages:
      # if it is the first inbound
      if (message.entry_direction == 'in') and not set_in:
        logging.debug('START TIMER')
        start_time = message.entry_datetime
        set_in = True
      # if outbound after series of inbound
      elif message.entry_direction == 'out' and set_in:
        message.timedelta_hours = convert_timedelta_to_hours(message.entry_datetime-start_time)
        start_time = None
        set_in = False
        logging.debug('RESET TIMER')

    final_data.extend(messages)
  return final_data


def persist_output_csv(data, output_path):
  csv_data = [message.to_dict() for message in data]
  keys = csv_data[0].keys()
  with open(output_path, 'w+') as output_file:
    dict_writer = DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(csv_data)
  logging.info(f'Output CSV written to: {output_path} ')
