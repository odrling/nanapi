CREATE MIGRATION m17r4sy23vrv4mvvuarlrduao6uslw3e2oaacgmzm5k66qcyslwh4q
    ONTO m1eyjzygebrxrqjnmi6nw52sp6wi2fuf42wb3oxqgmbnpmnzhefhva
{
  CREATE GLOBAL default::client := (SELECT
      default::Client
  FILTER
      (.id = GLOBAL default::client_id)
  );
  ALTER TYPE default::ClientObject {
      ALTER ACCESS POLICY client_rw USING ((GLOBAL default::client ?= .client));
  };
};
