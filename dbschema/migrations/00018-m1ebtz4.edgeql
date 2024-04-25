CREATE MIGRATION m1ebtz4vac7ldmn7yyir3mzfq6efubespf6k5kzrr3eqslesj6grka
    ONTO m1xd2figtmwahmf7rrxig5wqvnnqcfiwrhlvhqdv3wvspxnaan43fa
{
  ALTER TYPE projection::Projection {
      ALTER LINK external_medias {
          CREATE PROPERTY added: std::datetime {
              SET default := (std::datetime_of_statement());
              SET readonly := true;
          };
      };
      ALTER LINK medias {
          CREATE PROPERTY added: std::datetime {
              SET default := (std::datetime_of_statement());
              SET readonly := true;
          };
      };
  };
};
