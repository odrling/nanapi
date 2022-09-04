with
  code := <str>$code,
delete waicolle::Coupon
filter .client = global client and .code = code
