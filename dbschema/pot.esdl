module pot {
  type Pot extending default::ClientObject {
    required property amount -> float32 {
      constraint min_value(0.0);
      default := 0.0;
    }
    required property count -> int32 {
      default := 0;
    }
    required link user -> user::User {
      on target delete delete source;
    }
    constraint exclusive on ((.client, .user));
  }
}
