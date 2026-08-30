// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-a7ebb22e
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { getDb } from "../api/queries/connection";
// TODO: import tables from "./schema"

async function seed() {
  const db = getDb();
  console.log("Seeding database...");

  // TODO: insert seed data, e.g.
  // await db.insert(schema.posts).values([
  //   { title: "First post", content: "Hello world" },
  // ]);

  console.log("Done.");
  process.exit(0); // close MySQL connection pool
}

seed();
