-- SQL dump generated using DBML (dbml.dbdiagram.io)
-- Database: PostgreSQL
-- Generated at: 2025-10-06T19:49:51.177Z

CREATE TABLE "users" (
  "id" int UNIQUE NOT NULL,
  "email" varchar(255) UNIQUE NOT NULL,
  "name" varchar(200),
  "created_at" timestamp NOT NULL
);

CREATE TABLE "products" (
  "id" int UNIQUE NOT NULL,
  "sku" varchar(64) UNIQUE NOT NULL,
  "title" varchar(255) NOT NULL,
  "price_jpy" decimal(10,2) NOT NULL,
  "is_active" boolean NOT NULL
);

CREATE TABLE "orders" (
  "id" int UNIQUE NOT NULL,
  "user_id" int NOT NULL,
  "ordered_at" timestamp NOT NULL,
  "status" varchar(32) NOT NULL,
  "total_jpy" decimal(12,2) NOT NULL
);

CREATE TABLE "order_items" (
  "id" int UNIQUE NOT NULL,
  "order_id" int NOT NULL,
  "product_id" int NOT NULL,
  "qty" int NOT NULL,
  "unit_price" decimal(10,2) NOT NULL
);

COMMENT ON COLUMN "users"."id" IS 'ユーザーの内部ID（後でpk指定予定）';

COMMENT ON COLUMN "users"."email" IS 'メールアドレス';

COMMENT ON COLUMN "users"."name" IS '表示名';

COMMENT ON COLUMN "users"."created_at" IS '作成日時（UTC）';

COMMENT ON COLUMN "products"."id" IS '商品ID（後でpk指定予定）';

COMMENT ON COLUMN "products"."sku" IS '在庫管理用SKU';

COMMENT ON COLUMN "products"."title" IS '商品名';

COMMENT ON COLUMN "products"."price_jpy" IS '価格（JPY）';

COMMENT ON COLUMN "products"."is_active" IS '販売中フラグ';

COMMENT ON COLUMN "orders"."id" IS '注文ID（後でpk指定予定）';

COMMENT ON COLUMN "orders"."user_id" IS 'users.id への外部参照の想定';

COMMENT ON COLUMN "orders"."ordered_at" IS '注文日時（UTC）';

COMMENT ON COLUMN "orders"."status" IS '注文状態（pending/shippedなど）';

COMMENT ON COLUMN "orders"."total_jpy" IS '合計金額（税送料込）';

COMMENT ON COLUMN "order_items"."id" IS '明細ID（後でpk指定予定）';

COMMENT ON COLUMN "order_items"."order_id" IS 'orders.id への外部参照の想定';

COMMENT ON COLUMN "order_items"."product_id" IS 'products.id への外部参照の想定';

COMMENT ON COLUMN "order_items"."qty" IS '数量';

COMMENT ON COLUMN "order_items"."unit_price" IS '単価（注文時点）';

ALTER TABLE "users" ADD FOREIGN KEY ("id") REFERENCES "orders" ("user_id");

ALTER TABLE "orders" ADD FOREIGN KEY ("id") REFERENCES "order_items" ("order_id");
