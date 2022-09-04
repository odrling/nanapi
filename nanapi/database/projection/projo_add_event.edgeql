with
  id := <uuid>$id,
  date := <datetime>$date,
  description := <str>$description,
  projo := (select projection::Projection filter .id = id)
insert projection::Event {
  client := global client,
  date := date,
  description := description,
  projection := projo
}
