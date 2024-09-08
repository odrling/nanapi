with
  id := <optional uuid>$id,
  status := <optional projection::Status>$status,
  message_id := <optional int64>$message_id,
  channel_id := <optional int64>$channel_id,
  all_projos := (select projection::Projection filter .client = global client),
  filtered := (
    (select all_projos filter .id = id)
    if exists id else
    (select all_projos filter .status = status and .channel_id = channel_id)
    if exists status and exists channel_id else
    (select all_projos filter .status = status)
    if exists status else
    (select all_projos filter .message_id = message_id)
    if exists message_id else
    (select all_projos filter .channel_id = channel_id)
    if exists channel_id else
    (select all_projos)
  )
select filtered {
  id,
  name,
  status,
  message_id,
  message_id_str,
  channel_id,
  channel_id_str,
  medias: {
    id_al,
    title_user_preferred,
    @added,
  } order by @added,
  external_medias: {
    id,
    title,
    @added,
  } order by @added,
  participants: { * },
  events: {
    date,
    description,
  }
}
