with
  id := <uuid>$id,
  title := <str>$title,
  _external := (
    insert projection::ExternalMedia {
      client := global client,
      title := title
    }
  )
update projection::Projection
filter .id = id
set { external_medias += _external }
