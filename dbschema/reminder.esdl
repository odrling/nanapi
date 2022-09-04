module reminder {
  type Reminder extending default::ClientObject {
    required link user -> user::User {
      on target delete delete source;
    }
    required property channel_id -> int64;
    required property channel_id_str := <str>.channel_id;
    required property timestamp -> datetime;
    required property message -> str;
  }
}
