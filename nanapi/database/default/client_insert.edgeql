with
  username := <str>$username,
  password_hash := <str>$password_hash,
insert Client {
  username := username,
  password_hash := password_hash,
}
