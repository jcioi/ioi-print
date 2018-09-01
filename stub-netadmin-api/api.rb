require 'sinatra/base'
require 'json'

class NetAdminAPI < Sinatra::Base
  get '/machines/lookup' do
    [
      200,
      {Rack::CONTENT_TYPE => 'application/json'},
      [JSON.dump(node_data(params['ip']))],
    ]
  end

  get '/desks/:id/map' do
    [
      200,
      {Rack::CONTENT_TYPE => 'image/svg+xml'},
      [map_data(params['id'])],
    ]
  end

  private

  def node_data(ip)
    {
      machine: {
        ip: ip,
        mac: '00:00:00:00:00:00',
      },
      contestant: {
        id: 'JPN-1',
        name: 'Morumotto Reloaded',
        special_requirement_note: 'Some remarks for this contestant.',
      },
      desk: {
        zone: 'arena',
        map: "http://netadmin-api/desks/A-10/map",
        id: 'A-10',
      },
    }
  end

  def map_data(id)
    IO.read('assets/desk_map.svg')
  end
end
