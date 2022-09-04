select histoire::Histoire {
  id,
  title,
  text,
  formatted,
}
filter .id = <uuid>$id
