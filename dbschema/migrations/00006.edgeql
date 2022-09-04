CREATE MIGRATION m1sc57pjblk5f5frr2toei7qv5ihtys6dplsy3g3rrf3mcg3el6uqa
    ONTO m1vxcphcfjbyrzeyuynbvg6yfhod5yxz4z2wigudtnsl77bldmjblq
{
  ALTER TYPE default::ClientObject {
      ALTER ACCESS POLICY client_access_rw RENAME TO client_rw;
  };
  ALTER TYPE default::ClientObject {
      ALTER ACCESS POLICY client_access_ro {
          RESET EXPRESSION;
          RENAME TO everyone_ro;
      };
  };
};
