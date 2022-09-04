with
  id := <uuid>$id,
  status := <projection::Status>$status,
update projection::Projection
filter .id = id
set { status := status }
