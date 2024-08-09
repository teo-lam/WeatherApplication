SELECT
    p.Locatie AS Location,
    p.ID AS PersonID,
    v.quality AS Quality
FROM
    persons p
        LEFT JOIN
    Votes v ON p.ID = v.chosen_person
ORDER BY
    v.quality NULLS LAST;
