-- create table
CREATE TABLE "public"."task_admin" (
  "task_id" serial,
  "extent" varchar(255) COLLATE "pg_catalog"."default",
  "originalextent" varchar(255) COLLATE "pg_catalog"."default",
  "user_id" varchar(50),
  "area_code" varchar(50),
  "handler" varchar(50) COLLATE "pg_catalog"."default",
  "state" int2 DEFAULT 1,
  "status" int2 DEFAULT 1,
  "created_at" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "end_at" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "task_admin_pkey" PRIMARY KEY ("task_id")
)
;
ALTER TABLE "public"."task_admin" 
  OWNER TO "postgres";

-- add COMMENT
COMMENT ON COLUMN "public"."task_admin"."task_id" IS '自增序列';
COMMENT ON COLUMN "public"."task_admin"."extent" IS '预测范围';
COMMENT ON COLUMN "public"."task_admin"."originalextent" IS '初始范围';
COMMENT ON COLUMN "public"."task_admin"."user_id" IS '用户编号';
COMMENT ON COLUMN "public"."task_admin"."area_code" IS '区划代码';
COMMENT ON COLUMN "public"."task_admin"."state" IS '当前状态';
COMMENT ON COLUMN "public"."task_admin"."status" IS '是否删除';
COMMENT ON COLUMN "public"."task_admin"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."task_admin"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."task_admin"."end_at" IS '完成时间';
COMMENT ON COLUMN "public"."task_admin"."handler" IS '预测主机';

-- create update function
CREATE OR REPLACE FUNCTION task_update_timestamp () RETURNS TRIGGER AS $$ BEGIN
		NEW.updated_at = CURRENT_TIMESTAMP;
	RETURN NEW;
END $$ LANGUAGE plpgsql;

-- create trigger on task
CREATE TRIGGER "task_upd" BEFORE UPDATE ON "public"."task_admin" FOR EACH ROW
EXECUTE PROCEDURE "public"."task_update_timestamp"();