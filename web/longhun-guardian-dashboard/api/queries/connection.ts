// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-4bb8d97c
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { drizzle } from "drizzle-orm/mysql2";
import { env } from "../lib/env";
import * as schema from "@db/schema";
import * as relations from "@db/relations";

const fullSchema = { ...schema, ...relations };

let instance: ReturnType<typeof drizzle<typeof fullSchema>>;

export function getDb() {
  if (!instance) {
    instance = drizzle(env.databaseUrl, {
      mode: "planetscale",
      schema: fullSchema,
    });
  }
  return instance;
}
