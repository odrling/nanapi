with
  username := <str>$username,
select Client {
  id,
  username,
  password_hash,
}
filter .username = username
