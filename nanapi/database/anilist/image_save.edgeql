with
  url := <str>$url,
  data := <str>$data,
insert anilist::Image {
  url := url,
  data := data,
}
unless conflict;
