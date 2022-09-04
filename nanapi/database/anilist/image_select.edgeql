with
  urls := <array<str>>$urls,
select anilist::Image {
  url,
  data,
}
filter .url in array_unpack(urls)
