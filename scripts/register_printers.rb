#!/usr/bin/env ruby

require 'pathname'
require 'shellwords'
require 'yaml'

PRINTERS_YML = Pathname(__dir__) / '../printers.yml'
DOCKER_COMPOSE_YML = Pathname(__dir__) / '../docker-compose.yml'

def exec(command)
  puts ">> #{command.shelljoin}"
  system(*%W[docker-compose -f #{DOCKER_COMPOSE_YML} exec cups-back], *command)
  puts "<< #$?"
end

YAML.load_file(PRINTERS_YML).each do |klass, devices|
  devices.each do |device|
    exec %W[lpadmin -p #{device.fetch('name')} -v #{device.fetch('uri')} -m #{device.fetch('model')} -E]
    exec %W[lpadmin -p #{device.fetch('name')} -c #{klass}]
  end
  exec %W[cupsenable #{klass}]
  exec %W[cupsaccept #{klass}]
end
