FROM ruby:2.5
WORKDIR /srv/admin-api

COPY Gemfile* /srv/admin-api/
RUN bundle install --deployment

COPY *.rb *.ru /srv/admin-api/
COPY assets/ /srv/admin-api/assets/

EXPOSE 80
ENTRYPOINT ["/usr/bin/env", "bundle", "exec"]
CMD ["rackup", "-p", "80", "-o", "0.0.0.0"]
