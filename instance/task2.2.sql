SELECT
    p.Locatie AS Location,
    COUNT(v.ID) AS NumberOfVotes
FROM
    persons p
        LEFT JOIN
    Votes v ON p.ID = v.chosen_person
GROUP BY
    p.Locatie;
