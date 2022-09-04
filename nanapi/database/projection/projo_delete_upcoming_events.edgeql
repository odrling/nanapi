with
  id := <uuid>$id,
  projo := (select projection::Projection filter .id = id)
delete projection::Event
filter .projection = projo and .date > datetime_current()
