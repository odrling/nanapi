module amq {
  type Account {
    required property username -> str {
      constraint exclusive;
    }
    required link user -> user::User {
      constraint exclusive;
      on target delete delete source;
    }
    index on (.username);
  }

  type Setting extending default::ClientObject {
    required property key -> str;
    required property value -> str;
    constraint exclusive on ((.client, .key));
  }
}
