begin transaction;

create table new_vote (
  id integer primary key autoincrement,
  name text not null,
  votes integer not null,
  addr text not null,
  time integer not null,
  totalvotes integer not null
);

insert into new_vote (name, votes, addr, time, totalvotes) select * from vote;
drop table vote;

alter table new_vote rename to vote;
create index vote_idx on vote(id,name,votes,totalvotes);

commit;
