#!/usr/bin/env python3
import http.server
import logging
from urllib.parse import urlparse
from os import path
import json

PORT = 10418
# Handler to deal with rhttp requests
Handler = http.server.SimpleHTTPRequestHandler

# Front_end file directory, note: Only allow the need one to protect your other files
curdir = path.dirname(path.realpath(__file__)) + '/front_end/public'
sep = '/'

# MIME-TYPE, Allowable file type
mimedic = [
        ('.html', 'text/html'),
        #('.htm', 'text/html'),
        ('.js', 'application/javascript'),
        ('.css', 'text/css'),
        #('.json', 'application/json'),
        #('.png', 'image/png'),
        #('.jpg', 'image/jpeg'),
        #('.gif', 'image/gif'),
        #('.txt', 'text/plain'),
        #('.avi', 'video/x-msvideo'),
        ]
# Test json
json_data = {
    "name": "test",
    "children":[
        {"name":"ga",
            "children":[
                {"name":"a", "value":2}, 
                {"name":"c", "value":2}, 
                {"name":"b", "value":2}]},
        {"name":"ga",
            "children":[
                {"name":"a", "value":2}, 
                {"name":"c", "value":2}, 
                {"name":"b", "value":2}]}]
}

# Class to handle http request
class RequestHandler(Handler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        #self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

        # Parse path and query
        querypath = urlparse(self.path)
        filepath, query = querypath.path, querypath.query 

        # Get new keyword from front-end
        if filepath.endswith('/keyword'):
            logging.info("Get keyword: " + query)
            self.send_response(200)
            self.send_header('Content-type', 'json')
            self.end_headers()
            # Write back correlation json file
            self.wfile.write(json.dumps(json_data).encode('utf-8'))
        # By default, redirect to index.html
        elif filepath.endswith('/'):
            filepath += 'index.html'
        # Parse each request to send back file
        else:
            sendReply = False
             filename, fileext = path.splitext(filepath)
             # Check the request file is legal
             for e in mimedic:
                 if e[0] == fileext:
                     mimetype = e[1]
                     sendReply = True

             if sendReply == True:
                 try:
                     with open(path.realpath(curdir + sep + filepath),'rb') as f:
                         content = f.read()
                         self.send_response(200)
                         self.send_header('Content-type',mimetype)
                         self.end_headers()
                         self.wfile.write(content)
                 except IOError:
                     self.send_error(404,'File Not Found: %s' % self.path)

def server_run():
    logging.info('Starting httpd...\n')
    httpd = http.server.HTTPServer(("", PORT), RequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

def main():
    server_run()

if(__name__ == "__main__"):
    main()
