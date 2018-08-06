require 'sinatra/base'
require 'json'

class NetAdminAPI < Sinatra::Base
  get '/api/nodes/ip/:ip/' do
    [
      200,
      {Rack::CONTENT_TYPE => 'application/json'},
      [JSON.dump(node_data(params['ip']))],
    ]
  end

  get '/api/nodes/ip/:ip/map/' do
    [
      200,
      {Rack::CONTENT_TYPE => 'image/svg+xml'},
      [map_data(params['ip'])],
    ]
  end

  private

  def node_data(ip)
    {
      node: {
        ip: ip,
        mac: '00:00:00:00:00:00',
      },
      contestant: {
        id: 'JPN-1',
        country: 'JPN',
        number: '1',
        name: 'Morumotto Reloaded',
      },
      desk: {
        zone: 'A',
        number: 10,
        map: "/api/nodes/ip/#{ip}/map/",
        id: 'A-10',
      },
    }
  end

  def map_data(ip)
    IO.read('assets/desk_map.svg')
  end
end
