# Overview

Work / code related to rebuilding of the contaminated sites registry application
which is currently hosted @ BCOnline.  BC Online app satisfies the legislative
requirement of making contaminated sites information available.  Contaminated
Sites data is provided on a cost recovery basis.  Billing is handled by
BC Online

# Background Material

* [Confluence: Architectural Response Document](https://apps.nrs.gov.bc.ca/int/confluence/pages/viewpage.action?pageId=91201900)
* [Confluence: BC Online Data Analysis](https://apps.nrs.gov.bc.ca/int/confluence/display/AR/BC+Online+Data+Analysis)
* [Sample BC Online Report](https://apps.nrs.gov.bc.ca/int/confluence/display/AR/BC+Online+Data+Analysis?preview=/104733220/104733210/bconline_sample_report.txt)
* [S3 Bucket with Sample Data](https://nrs.objectstore.gov.bc.ca/epdsbx/dbdump)

# Modernization / Rebuilding Approach

* Redirect operation contaminated sites database dumps from BC Online ftp
  site to S3 bucket.
* Openshift postgres database will load the bc online data.
* Application will be rebuilt using a services based approach, with backend
    api and frontend that consumes it
* Backend api app will not be available outside of openshift namespace.
* Payment: how this will be handled has not been determined.

