CREATE MIGRATION m1x4rw6dlkx7krzqinbvzztwjq35v7agbbwpthklybfywfjk7dwrka
    ONTO m1n2saa24miuujihs3er6idi2bphct3bxohztethbtmbobgbra5fwa
{
  CREATE MODULE redis IF NOT EXISTS;
  CREATE TYPE redis::Data {
      CREATE REQUIRED PROPERTY key -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE INDEX ON (.key);
      CREATE REQUIRED PROPERTY value -> std::str;
  };
};
