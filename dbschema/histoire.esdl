module histoire {
  type Histoire extending default::ClientObject {
    required property title -> str;
    required property text -> str;
    required property formatted -> bool {
      default := true;
    }
    constraint exclusive on ((.client, .title));
  }
}
