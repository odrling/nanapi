with
  id := <uuid>$id,
  name := <str>$name,
update projection::Projection
filter .id = id
set { name := name }
