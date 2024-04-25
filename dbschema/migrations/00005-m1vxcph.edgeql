CREATE MIGRATION m1vxcphcfjbyrzeyuynbvg6yfhod5yxz4z2wigudtnsl77bldmjblq
    ONTO m1x4rw6dlkx7krzqinbvzztwjq35v7agbbwpthklybfywfjk7dwrka
{
  ALTER TYPE default::ClientObject {
      ALTER ACCESS POLICY client_access RENAME TO client_access_rw;
  };
  ALTER TYPE default::ClientObject {
      CREATE ACCESS POLICY client_access_ro
          ALLOW SELECT USING (EXISTS ((SELECT
              default::Client
          FILTER
              (.id = GLOBAL default::client_id)
          )));
  };
};
