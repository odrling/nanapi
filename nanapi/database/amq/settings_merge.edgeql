with
  settings := <json>$settings,
for setting in json_object_unpack(settings) union (
  with
    key := <str>setting.0,
    value := <str>to_str(setting.1),
  insert amq::Setting {
    client := global client,
    key := key,
    value := value,
  }
  unless conflict on ((.client, .key))
  else (
    update amq::Setting set {
      value := value,
    }
  )
);
