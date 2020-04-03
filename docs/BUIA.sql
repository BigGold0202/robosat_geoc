-- add pgis extension
CREATE extension postgis;

-- create table
CREATE TABLE "public"."BUIA" (
  "gid" serial4,
  "CNAME" varchar(255) COLLATE "pg_catalog"."default",
  "LEVEL" varchar(20) COLLATE "pg_catalog"."default",
  "geom" "public"."geometry",
  CONSTRAINT "BUIA_pkey" PRIMARY KEY ("gid")
)
;

ALTER TABLE "public"."BUIA" 
  OWNER TO "postgres";

-- create index
CREATE INDEX "BUIA_geom_idx" ON "public"."BUIA" USING gist (
  "geom" "public"."gist_geometry_ops_2d"
);

CREATE INDEX "BUIA_gid_idx" ON "public"."BUIA" USING btree (
  "gid" "pg_catalog"."int4_ops" ASC NULLS LAST
)
