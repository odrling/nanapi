module role {
  type Role extending default::ClientObject {
    required property role_id -> int64;
    required property role_id_str := <str>.role_id;
    required property emoji -> str;
    constraint exclusive on ((.client, .role_id));
    constraint exclusive on ((.client, .emoji));
    index on (.role_id);
  }
}
