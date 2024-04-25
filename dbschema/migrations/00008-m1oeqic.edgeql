CREATE MIGRATION m1oeqicjcprimj2u5wnmvsbfhzpasoiebcmfo32vtszcqpr6umt5ja
    ONTO m1sbjqlnruo6x7qems6ukwa53puo3vsogettkok2dnhrcyin2wgcrq
{
  ALTER TYPE default::ClientObject {
      CREATE ACCESS POLICY everyone_ro
          ALLOW SELECT ;
  };
};
