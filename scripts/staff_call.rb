#!/usr/bin/env ruby
require 'json'
require 'uri'
require 'net/http'

PRINT_SERVER=URI("http://localhost:5000")

unless ARGV.size == 4
   $stderr.puts <<EOF
Illegal number of arguments
Usage: staff_call.rb REQUEST_MSG CONTESTANT_ID CONTESANT_NAME DESK_ID
EOF
  exit 1
end

message, contestant_id, contestant_name, desk_id = *ARGV

payload = {
  message: message,
  contestant: {
    id: contestant_id,
    name: contestant_name,
  },
  desk: {
    id: desk_id,
  },
}

http = Net::HTTP.new(PRINT_SERVER.host, PRINT_SERVER.port)
http.use_ssl = PRINT_SERVER.is_a?(URI::HTTPS)

http.post2('/staff_call', JSON.dump(payload),
           'Content-Type' => 'application/json') do |res|
  puts res.body
end
