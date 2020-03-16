-- create table
CREATE TABLE "public"."task" (
  "task_id" serial,
  "extent" varchar(255) COLLATE "pg_catalog"."default",
  "user_id" varchar(50),
  "area_code" varchar(50),
  "state" int2 DEFAULT 1,
  "status" int2 DEFAULT 1,
  "created_at" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "end_at" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "handler" varchar(255),
  CONSTRAINT "task_pkey" PRIMARY KEY ("task_id")
)
;
ALTER TABLE "public"."task" 
  OWNER TO "postgres";

-- add COMMENT
COMMENT ON COLUMN "public"."task"."task_id" IS '自增序列';
COMMENT ON COLUMN "public"."task"."extent" IS '预测范围';
COMMENT ON COLUMN "public"."task"."user_id" IS '用户编号';
COMMENT ON COLUMN "public"."task"."area_code" IS '区划代码';
COMMENT ON COLUMN "public"."task"."state" IS '当前状态';
COMMENT ON COLUMN "public"."task"."status" IS '是否删除';
COMMENT ON COLUMN "public"."task"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."task"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."task"."end_at" IS '完成时间';

-- create update function
CREATE OR REPLACE FUNCTION task_update_timestamp () RETURNS TRIGGER AS $$ BEGIN
		NEW.updated_at = CURRENT_TIMESTAMP;
	RETURN NEW;
END $$ LANGUAGE plpgsql;

-- create trigger on task
CREATE TRIGGER "task_upd" BEFORE UPDATE ON "public"."task" FOR EACH ROW
EXECUTE PROCEDURE "public"."task_update_timestamp"();