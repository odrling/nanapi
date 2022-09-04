with
  role_id := <int64>$role_id,
delete role::Role
filter .client = global client and .role_id = role_id
