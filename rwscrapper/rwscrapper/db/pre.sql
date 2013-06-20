drop database if exists rwscrapper;
create database rwscrapper character set utf8 collate utf8_general_ci;;

drop user 'scrapper'@'localhost';
create user 'scrapper'@'localhost' identified by 'scrapper';

use rwscrapper;

grant all on rwscrapper.* to 'scrapper'@'localhost';
grant all on DEX.* to 'scrapper'@'localhost';
grant super on *.* to 'scrapper'@'localhost';

drop table if exists `Texts`;
create table `Texts` (
    `textId` int not null auto_increment,
    `url` char(200) not null,
    `canonicalUrl` char(200) not null,
    `contentFile` text character set utf8 not null,
    `trigramError` float(4,2) not null,
    `bigramError` float(4,2) not null,
    `unigramError` float(4, 2) not null,
    `freqError` float(4, 2) not null,
    `averageWordLength` float(5, 2) not null,
    `romanianScore` float(4, 2) not null,
    `sourceType` int(11) not null,
    `createDate` int(11) not null,
    primary key(`id`),
    index(`id`)
);

drop table if exists `Phrases`;
create table `Phrases` (
    `id` int(11) not null auto_increment,
    `textId` int not null,
    `phraseContent` text character set utf8 not null,
    `romanianScore` float(11,2) not null,
    primary key(`id`),
    foreign key(`textId`) references Texts(`id`),
    index(`id`)
);

drop table if exists `Prefixes`;
create table `Prefixes` (
    `id` int(11) not null auto_increment,
    `form` char(20) collate utf8_romanian_ci not null,
    `formUtf8General` char(20) character set utf8 not null,
    `prefixLength` int(11) not null,
    `meaning` text collate utf8_romanian_ci,
    primary key(`id`),
    index(`id`),
    index(`form`)
);

drop table if exists `Suffixes`;
create table `Suffixes` (
    `id` int(11) not null auto_increment,
    `form` char(20) collate utf8_romanian_ci not null,
    `formUtf8General` char(20) character set utf8 not null,
    `suffixLength` int(11) not null,
    `meaning` text collate utf8_romanian_ci,
    primary key(`id`),
    index(`id`),
    index(`form`)
);

drop table if exists `Domains`;
create table `Domains` (
    id int(11) not null auto_increment,
    name char(100) collate utf8_romanian_ci not null,
    primary key(`id`),
    index(`id`),
    index(`name`)
);


drop table if exists `Words`;
create table `Words` (
    `id` int(11) not null auto_increment,
    `phraseId` int(11) not null,
    `form` char(100) collate utf8_romanian_ci not null,
    `formUtf8General` char(100) character set utf8 not null,
    `reverse` char(100) collate utf8_romanian_ci not null,
    `charLength` int(11) not null,
    `createDate` int(11) not null,
    `etymology` varchar(50),
    `suffixId` int(11),
    `prefixId` int(11),
    `domainId` int(11),
    `definition` text collate utf8_romanian_ci,
    primary key(`id`),
    foreign key(`phraseId`) references Phrases(`id`),
    foreign key(`prefixId`) references Prefixes(`id`),
    foreign key(`suffixId`) references Suffixes(`id`),
    foreign key(`domainId`) references Domains(`id`),
    index(`id`),
    index(`form`)
);

drop table if exists `Inflections`;
create table `Inflections` (
    `id` int(11) not null auto_increment,
    `description` varchar(255) collate utf8_romanian_ci,
    `shortForm` varchar(10),
    primary key(`id`),
    index(`id`)
);

drop table if exists `InflectedForms`
create table `InflectedForms` (
    `id` int(11) not null auto_increment,
    `wordId` int(11) not null,
    `inflectionId` int(11) not null,
    `form` char(100) collate utf8_romanian_ci not null,
    `formUtf8General` char(100) character set utf8 not null,
    `noApp` int(11) default 1,
    primary key(`id`),
    foreign key(`wordId`) references Words(`id`),
    foreign key(`inflectionId`) references Inflections(`id`),
    index(`id`),
    index(`form`)
);

lock tables `Inflections` write;
insert into `Inflections` values
