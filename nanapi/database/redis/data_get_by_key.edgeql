with
  key := <str>$key,
select redis::Data {
  key,
  value,
}
filter .key = key
