with
  id := <uuid>$id,
  message_id := <int64>$message_id,
update projection::Projection
filter .id = id
set { message_id := message_id }
