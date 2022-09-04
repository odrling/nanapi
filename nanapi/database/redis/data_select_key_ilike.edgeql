with
  pattern := <str>$pattern,
select redis::Data {
  key,
}
filter .key ilike pattern
