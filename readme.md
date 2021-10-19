# Overview

Work / info related to comparing bconline site app with the data export
to provide some level of certainty that the data in the mainframe app is
entirely provided by the oracle data dump.

* [bconline url](https://www.bconline.gov.bc.ca/)
* [bconline app docs](https://t1.bconline.gov.bc.ca/pdf/site_reg.pdf)
* [site svn](https://a100.gov.bc.ca/pub/svn/sis/)
* [jira ticket](https://apps.nrs.gov.bc.ca/int/jira/browse/SD-29501)

# crontab config: https://a100.gov.bc.ca/pub/svn/sis/trunk/admin/crontab.cfg

```
#{bconline_schedule} /apps_ux/sis/admin/bconline.sh 2>&1 | /apps_ux/oraapp/bin/mailtee.ksh /apps_ux/sis/logs/bconline.sh.log sitelogs@Victoria1.gov.bc.ca bconline.sh true
```

order of operation
1. crontab calls bconline.sh
1. bconline.sh calls: srdump.sql
1. simulated running the script by dumping:
    - @srdate
    - @srsites
    - @srevents
    - @srevpart
    - @srpinpid
    - @srsitpar
    - @srparrol
    - @srsitdoc
    - @srdocpar
    - @srlands
    - @srassocs
    - @srprofil
    - @srprfans
    - @srprfuse
    - @srprfcat
    - @srprfque

The resulting *.lis files have been copied to the directory: sampledata

==========================================================================

Report Verification
--------------------------------------------------------------------------

On BCOnline ran report against:
Parcel id = 008006148

Resulting bconline detailed report is in: bconline_sample_report.txt

The following section describes the mapping of data in the report with tables
and columns in the dumped data.

Summary / Start Section
---------------------------------------------------------------------------

site id                                 srpinpid    (columm 1) = 0000000009
parcel id                               srpinpid    (column 2) = 008006148
lat longs                               srsites     (columns 10 - 16)

Victoria File / Regional File           srsites     (columns 17 - 18)
Region                                  srsites     (column 2)
Site Address                            srsites     (column 4)
site city                               srsites     (column 6)
site province                           srsites     (column 7)
site postal code                        srsites     (column 8)
registered / updated / removed dates    srsites     (last 3 columns)

Notations (total number)                srevents    (column 1) - column 1 is the siteid, counts matching records
Participants (total number)             srsitpar    (column 1) - column 1 is the siteid, counts matching records
associated sites (total number)         srassocs    (column 1) - column 1 is the siteid, counts matching records
documents (total number)                srsitdoc    (column 1) - column 1 is the siteid, counts matching records
susp. Land Use (total number)           srlands     (column 1) - column 1 is the siteid,   Guess as records match
parcel descriptions (total number)      srpinpid    (column 1) - column 1 is the siteid... Guess
Location Description:                   srsites     (near end)
Record Status                           srsites     (column 3)
Fee category                            srsites

Individual notation Section
---------------------------------------------------------------------------
Notation Type                           srevents    (column 3)
Notation Class                          srevents    (column 4)
Initiated                               srevents    (column 5)
Approved                                srevents    (column 6)
Ministry Contact                        srevents    (column 7)
Notation Participants                   srevents->srevpart 1->Many    (column 2)
Notation Roles                          srevents->srevpart 1->Many   (column 3)
Note                                    srevents->srevpart 1->Many   (column 8)
Required Actions                        srevents->srevpart 1->Many   (column 9)

Individual Participant Section
---------------------------------------------------------------------------
Participant:                            srsitpar    (column 3)
Roles                                   srsitpar->srparrol(one to many) (column 2)
Start Date                              srsitpar    (column 4)

Documents Section
---------------------------------------------------------------------------
Title                                   srsitdoc (column 3)
Authored                                srsitdoc (column 5)
Submitted                               srsitdoc (column 6)
Participants                            srdocpar (column 2)
Role                                    srdocpar (column 3)
Notes                                   srsitdoc (column 7)

Associated Sites Section
---------------------------------------------------------------------------
associated site id                      srassocs (column 2)
associated site date                    srassocs (column 3)
associated site notes                   srassocs (column 4)

Suspected Land Use Section
---------------------------------------------------------------------------
Description                             srlands (column 2)
Notes                                   srlands (column 3)

Parcel Descriptions Section
---------------------------------------------------------------------------
Date Added                              srpinpid (column 4)
Crown Land PIN#                         srpinpid ??? - not filled in report that ran
LTO PID#                                srpinpid (column 2)
Crown Land File#                        ??? - not filled in report that I ran
Land Desc                               srpinpid (column 3)

Current Site Profile Information Section
---------------------------------------------------------------------------
Site Profile Completion Date            srprfuse (column 2)
Site Profile Completion Date (also here)srprofil (column 6)
Ministry Regional Manager Received      srprofil (column 2)
Decision (date)                         srprofil (column 9)
Decision (outcome)                      srprofil (column 11)
Site Registrar Received                 ??
Entry Date                              ??
reference                               srprfuse (column 3)
Description                             srprfuse (column 4)

Areas of Potential Concern Section
---------------------------------------------------------------------------
This section is a linkage of the question / answer section

Section text                            srpfcat (column 5)
Question / statement                    srprfque (column 5)
Answer / applicable?                    srprfans (column 4)


==========================================================================

Relationships
--------------------------------------------
This isn't related to the report, but is instead a quick description of the relationships
in the tables.

srsites.siteid         (column 1)   ->  srevents.siteid (column 1)
srsites.siteid         (column 1)   ->  srpinpid.siteid (column 1)
srsites.siteid         (column 1)   ->  srassocs.siteid (column 1)
srsites.siteid         (column 1)   ->  srlands.siteid (column 1)
srsites.siteid         (column 1)   ->  srsitdoc.siteid (column 1)
srsitdoc.documentid    (column 2)   ->  srdocpar.documentid (column 1)
srsites.siteid         (column 1)   ->  srprfuse.siteid (column 1)
srsitpar.partcicipantid (column 2)  ->  srparrol.partcicipantid (column 1)
srsites.siteid         (column 1)   ->  srprofil.siteid(column 1)
srsites.siteid         (column 1)   ->  srprfans.siteid(column 1)
srprfans.questionid    (column 2)   ->  srprfque.questionid (column 1)
srprfque.questioncategory(column 3) ->  srprfcat.questioncategory (column 1)
srevents.participantid (column 2)   ->  srevpart.participantid (column 1)


==========================================================================

Table Descriptions
--------------------------------------------

srsitpar - participants
srsites -  sites
srevents - events
srevpart - event participants
srpinpid - pins and pids
srsitpar - participants
srparrol - participant roles
srsitdoc - site documents
srdocpar - site documents participants
srlands  - land histories
srassocs - associations
srprofil - profiles
srprfans - site profile answers
srprfuse - profile land uses
srprfcat - profile categories
srprfque - profile questions


# Conclusion

Looks like all the data is in there.  The only missing part is the fee structure
for how documents are charged, and a more complete understanding of how that works




