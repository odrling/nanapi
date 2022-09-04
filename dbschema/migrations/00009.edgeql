CREATE MIGRATION m1yvlmumz4lgdyae7v5xiy7bn4wgwqkocowg3jdacklvfhkfo5myxq
    ONTO m1oeqicjcprimj2u5wnmvsbfhzpasoiebcmfo32vtszcqpr6umt5ja
{
  ALTER TYPE default::Client {
      ALTER PROPERTY name {
          RENAME TO username;
      };
      CREATE INDEX ON (.username);
  };
};
