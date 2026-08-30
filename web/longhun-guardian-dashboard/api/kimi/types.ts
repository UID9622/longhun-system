// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-3c153b65
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
export type TokenResponse = {
  access_token: string;
  token_type: string;
  expires_in: number;
  refresh_token?: string;
  scope: string;
};

export type SessionPayload = {
  unionId: string;
  clientId: string;
};

export type UserProfile = {
  user_id: string;
  name: string;
  avatar_url: string;
};
