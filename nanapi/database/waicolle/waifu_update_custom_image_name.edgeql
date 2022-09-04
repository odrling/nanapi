with
  id := <uuid>$id,
  custom_image := <optional str>$custom_image,
  custom_name := <optional str>$custom_name,
update waicolle::Waifu
filter .id = id
set {
  custom_image := (
    (<str>{} if custom_image ilike '' else custom_image)
    if exists custom_image
    else .custom_image
  ),
  custom_name := (
    (<str>{} if custom_name ilike '' else custom_name)
    if exists custom_name
    else .custom_name
  ),
}
