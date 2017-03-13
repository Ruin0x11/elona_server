begin transaction;

-- log(en).txt format:
-- 7685733%1/04(10)%dead淑女の精霊サリーは盗賊の隠れ家で強盗に殺された。「今日は眠れないな」%1.95.255.124.ap.yournet.ne.jp%

drop table if exists chat;
create table chat (
  id integer primary key autoincrement,
  time int not null,     -- UNIX timestamp to be converted to [M/DD(HH)]
  kind tinyint not null, -- one of "chat" (0), "dead" (1) or "wish" (2)
  text text not null,    -- text of message
  addr text not null     -- IP address/website of player
);

-- vote(en).txt format:
-- 1<>十字の蛇scar<>53<>114.157.208.48<>1449840576#625#66#<>
-- (first digit is line no.)

drop table if exists vote;
create table vote (
  id integer primary key autoincrement,
  name text not null,          -- name of registrant
  votes integer not null,      -- number of votes
  addr text not null,          -- IP address of user
  time integer not null,       -- UNIX timestamp of last vote reset?
  totalvotes integer not null -- total votes across all resets?
);

create index vote_idx on vote(id,name,votes,totalvotes);

commit;
