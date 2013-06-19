drop database if exists rwscrapper;
create database rwscrapper character set utf8 collate utf8_general_ci;;

drop user 'scrapper'@'localhost';
create user 'scrapper'@'localhost' identified by 'scrapper';

use rwscrapper;

grant all on rwscrapper.* to 'scrapper'@'localhost';

drop table if exists Texts;
create table Texts (
    TextId int not null auto_increment,
    Url varchar(200) not null,
    CanonicalUrl varchar(200) not null,
    ContentFile varchar(100) not null,
    TrigramError float(4,2) not null,
    BigramError float(4,2) not null,
    UnigramError float(4, 2) not null,
    FreqError float(4, 2) not null,
    AverageWordLength float(5, 2) not null,
    RomanianScore float(4, 2) not null,
    Time timestamp null default current_timestamp,
    primary key(TextId),
    index(TextId)
);

drop table if exists Phrases;
create table Phrases (
    PhraseId int not null auto_increment,
    TextId int not null,
    PhraseContent text not null,
    RomanianScore float(10,2) not null,
    primary key(PhraseId),
    foreign key(TextId) references Texts(TextId),
    index(PhraseId)
);

drop table if exists Words;
create table Words (
    WordId int not null auto_increment,
    PhraseId int not null,
    Word varchar(200) not null,
    IsHyphenized boolean not null default false,
    IsLoan boolean not null default false,
    IsCommon boolean not null default false,
    IsArchaic boolean not null default false,
    IsRegional boolean not null default false,
    IsNeologism boolean not null default false,
    IsMisspelled boolean not null default false,
    Appearances int not null default 0,
    Domain varchar(50),
    Etymology varchar(10),
    Suffix varchar(20),
    Prefix varchar(20),
    PartOfSpeech varchar(50),
    StandardForm varchar(200),
    Definition text,
    primary key(WordId),
    foreign key(PhraseId) references Phrases(`PhraseId`),
    index(WordId),
    index(Word)
);
