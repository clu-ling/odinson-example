#!/usr/local/bin/python
from   typing    import Dict, Optional
import argparse
import json
import logging
import os
import sys
import requests


def query_index(
  url: str,
  grammar_file: str,
  # NOTE: the following are all optional in the API endpoint
  parent_query: Optional[str] = None,
  page_size: Optional[int] = 10,
  allow_trigger_overlaps: bool = False
) -> Dict:
  """
  Queries /api/execute/grammar and returns JSON response.
  """
  # API endpoint
  endpoint: str = f"{url}/api/execute/grammar"
  logging.debug(f"endpoint: {endpoint}")
  # load contents of grammar file
  abs_path: str = os.path.abspath(os.path.expanduser(grammar_file))
  logging.debug(f"abs_path: {abs_path}")
  with open(abs_path) as infile:
    grammar = infile.read()
  
  headers = {
    #"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64; rv:41.0) Gecko/20100101 Firefox/41.0",
    "Content-type": "application/json", "Accept": "application/json"
  }

  payload: Dict = {
    "grammar": grammar,
    "parentQuery": parent_query,
    "pageSize": page_size,
    "allowTriggerOverlaps": allow_trigger_overlaps
  }
  # remove k,v pairs where value is None
  payload = {k:v for k,v in payload.items() if v}

  logging.debug(f"payload: {payload}")

  response = requests.post(
    endpoint, 
    json=payload
  )
  logging.debug(response.text)
  logging.debug(f"status_code: {response.status_code}")

  logging.debug(f"request body: {response.request.body}")
  logging.debug(f"request headers: {response.request.headers}")
  if response.status_code != 200:
    logging.error(f"error: {response.reason}")
    return dict()
  return response.json()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode for debugging")

  parser.add_argument("-u", "--host", default="http://localhost:9000", dest="url", help="Base URL (and port) for api service.")

  parser.add_argument("-i", "--grammar", dest="grammar_file", required=True, help="YAML file defining odinson grammar")

  parser.add_argument("-p", "--parent-query", dest="parent_query", default=None, nargs="?", help="Odinson parentQuery for filtering documents by their metadata fields. Structured as a Lucene query (see http://www.lucenetutorial.com/lucene-query-syntax.html).")

  parser.add_argument("-s", "--page-size", dest="page_size", default=None, type=int, nargs="?", help="Odinson pageSize.  The maximum number of matches to return.")

  parser.add_argument("-a", "--allow-trigger-overlaps", dest="allow_trigger_overlaps", action="store_true", help="Odinson allowTriggerOverlaps.  Whether or not a match may overlap with a trigger.")

  args = parser.parse_args()

  logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG if args.verbose else logging.INFO,
  )

  logging.debug(f"url: {args.url}")
  logging.debug(f"grammar_file: {args.grammar_file}")
  logging.debug(f"parent_query: {args.parent_query}")
  logging.debug(f"page_size: {args.page_size}")
  logging.debug(f"allow_trigger_overlaps: {args.allow_trigger_overlaps}")

  response = query_index(
    url=args.url,
    grammar_file=args.grammar_file,
    parent_query=args.parent_query,
    page_size=args.page_size,
    allow_trigger_overlaps=args.allow_trigger_overlaps
  )

  print(json.dumps(response, sort_keys=True, indent=4))
