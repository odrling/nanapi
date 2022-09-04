with
  type := <presence::PresenceType>$type,
  name := <str>$name,
insert presence::Presence {
  client := global client,
  type := type,
  name := name,
}
