module presence {
  scalar type PresenceType extending enum<PLAYING, LISTENING, WATCHING>;

  type Presence extending default::ClientObject {
    required property type -> PresenceType;
    required property name -> str;
    constraint exclusive on ((.client, .type, .name));
  }
}
