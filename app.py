#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example for using the Google Search Analytics API (part of Search Console API).

A basic python command-line example that uses the searchAnalytics.query method
of the Google Search Console API. This example demonstrates how to query Google
search results data for your property. Learn more at
https://developers.google.com/webmaster-tools/

To use:
1) Install the Google Python client library, as shown at https://developers.google.com/webmaster-tools/v3/libraries.
2) Sign up for a new project in the Google APIs console at https://code.google.com/apis/console.
3) Register the project to use OAuth2.0 for installed applications.
4) Copy your client ID, client secret, and redirect URL into the client_secrets.json file included in this package.
5) Run the app in the command-line as shown below.

Sample usage:

  $ python search_analytics_api_sample.py 'https://www.example.com/' '2015-05-01' '2015-05-30'

"""
from __future__ import print_function

import argparse
import csv
import httpx
import os.path
import sys

from bs4 import BeautifulSoup
from googleapiclient import sample_tools
from googleapiclient.errors import HttpError

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('sitemap', type=str,
                       help=('Sitemap.'))
argparser.add_argument('start_date', type=str,
                       help=('Start date of the requested date range in '
                             'YYYY-MM-DD format.'))
argparser.add_argument('end_date', type=str,
                       help=('End date of the requested date range in '
                             'YYYY-MM-DD format.'))


def main(argv):
    service, flags = sample_tools.init(
        argv, 'searchconsole', 'v1', __doc__, __file__, parents=[argparser],
        scope='https://www.googleapis.com/auth/webmasters.readonly')

    # First run a query to learn which dates we have data for. You should always
    # check which days in a date range have data before running your main query.
    # This query shows data for the entire range, grouped and sorted by day,
    # descending; any days without data will be missing from the results.

    # Get top 10 queries for the date range, sorted by click count, descending.
    html_doc = httpx.get(flags.sitemap)
    soup = BeautifulSoup(html_doc, 'html.parser')

    url_list = [url.contents[0] for url in soup.find_all('loc')]
    print(f'# of domains to query: {url_list.__len__()}')
    request = {
        'startDate': flags.start_date,
        'endDate': flags.end_date,
        'dimensions': ['query'],
        'rowLimit': 10
    }
    for property_uri in url_list[:4]:
        print(f'Reading property data from: {property_uri}')
        try:
            response = execute_request(service, property_uri, request)
            csv_writer_file, data_file = prepare_csv(response)
            append_new_data(csv_writer_file, response['rows'], property_uri)
        except HttpError:
            print(f"Couldn't access query data from {property_uri}")

    if data_file:
        data_file.close()

def prepare_csv(resp):
    """Starts a file pointer to a csv file and writes the header to it

    Args:
        writer: The file writer.
        rows: The rows received from the request to be written.
        property_uri: The site or app URI to request data for.

    Returns:
        A data_file poiter to be closed and the csv_writer pointers
    """
    write_header = False
    if not os.path.isfile('data_file.csv'):
        header = list(resp['rows'][0].keys())
        header.append('url')
        write_header = True
    data_file = open('data_file.csv', 'a')
    csv_writer = csv.writer(data_file)
    if write_header:
        csv_writer.writerow(header)
    return csv_writer, data_file


def append_new_data(writer, rows, property_uri):
    """Appends new data to an prepared csv

    Args:
        writer: The file writer.
        rows: The rows received from the request to be written.
        property_uri: The site or app URI to request data for.

    Returns:
        A data_file poiter to be closed
    """
    for row in rows:
        row['keys'] = row['keys'][0]
        row['property'] = property_uri
        writer.writerow(row.values())

def execute_request(service, property_uri, request):
    """Executes a searchAnalytics.query request.

    Args:
        service: The searchconsole service to use when executing the query.
        property_uri: The site or app URI to request data for.
        request: The request to be executed.

    Returns:
        An array of response rows.
    """
    analitics = service.searchanalytics()

    print(analitics.__dir__())
    query = analitics.query(
        siteUrl=property_uri, body=request).execute()
    return query


if __name__ == '__main__':
    main(sys.argv)
