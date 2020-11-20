TRUNCATE TABLE api_cluster RESTART IDENTITY;

SELECT *
FROM api_cluster ac ;

/* 
 * psql -h covid-19.cjh1ctfac1pi.ap-southeast-1.rds.amazonaws.com -p 5432 -U postgres -d postgres
 * */
CREATE TEMP TABLE temp_api_cluster AS TABLE api_cluster WITH NO DATA;

SELECT *
FROM temp_api_cluster;

\COPY temp_api_cluster(latitude, longtitude, TIMESTAMP, CLUSTER, SOURCE)
FROM '/home/anonymous/Documents/MY_CC_23_3.csv' CSV HEADER;

UPDATE temp_api_cluster
SET
created_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
WHERE created_at IS NULL
OR updated_at IS NULL;

UPDATE temp_api_cluster
SET
id = NEXTVAL('api_cluster_id_seq'::REGCLASS)
WHERE id IS NULL;

INSERT INTO api_cluster SELECT *
FROM temp_api_cluster;

SELECT TO_TIMESTAMP(TIMESTAMP / 1000)
FROM api_cluster ac ;
