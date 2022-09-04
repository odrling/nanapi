with
  name := <str>$name,
  channel_id := <int64>$channel_id,
insert projection::Projection {
  client := global client,
  name := name,
  channel_id := channel_id,
}
