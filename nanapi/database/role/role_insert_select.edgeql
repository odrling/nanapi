with
  role_id := <int64>$role_id,
  emoji := <str>$emoji,
  role := (
    insert role::Role {
      client := global client,
      role_id := role_id,
      emoji := emoji,
    }
  )
select role {
  role_id,
  role_id_str,
  emoji,
}
