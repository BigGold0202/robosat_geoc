CREATE TABLE "public"."predict_buildings" (
  "gid" serial4,
	"task_id" serial4,
  "extent" varchar(255) COLLATE "pg_catalog"."default",
  "user_id" int4,
  "area_code" varchar(20) COLLATE "pg_catalog"."default",
  "handler" varchar(50) COLLATE "pg_catalog"."default",
  "state" int2 DEFAULT 1,
  "status" int2 DEFAULT 1,
  "created_at" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "geom" "public"."geometry",
  CONSTRAINT "predict_buildings_pkey" PRIMARY KEY ("gid")
)
;

ALTER TABLE "public"."predict_buildings" 
  OWNER TO "postgres";


-- add COMMENT
COMMENT ON COLUMN "public"."predict_buildings"."task_id" IS '自增序列';
COMMENT ON COLUMN "public"."predict_buildings"."extent" IS '预测范围';
COMMENT ON COLUMN "public"."predict_buildings"."user_id" IS '用户编号';
COMMENT ON COLUMN "public"."predict_buildings"."state" IS '当前状态';
COMMENT ON COLUMN "public"."predict_buildings"."status" IS '是否删除';
COMMENT ON COLUMN "public"."predict_buildings"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."predict_buildings"."updated_at" IS '更新时间';


CREATE INDEX "predict_buildings_geom_idx" ON "public"."predict_buildings" USING gist (
  "geom" "public"."gist_geometry_ops_2d"
);

CREATE INDEX "predict_buildings_gid_idx" ON "public"."predict_buildings" USING btree (
  "gid" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- create update function
CREATE OR REPLACE FUNCTION predict_buildings_update_timestamp () RETURNS TRIGGER AS $$ BEGIN
		NEW.updated_at = CURRENT_TIMESTAMP;
	RETURN NEW;
END $$ LANGUAGE plpgsql;

-- create trigger on task
CREATE TRIGGER "predict_buildings_upd" BEFORE UPDATE ON "public"."predict_buildings" FOR EACH ROW
EXECUTE PROCEDURE "public"."predict_buildings_update_timestamp"();