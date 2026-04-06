# API Reference

Full documentation for all 35 MCP tools and 4 resource URIs provided by the Washington State Legislature MCP Server.

## Bill Information Tools (8 tools)

### getBillInfo

Retrieves detailed information about a specific bill using the GetLegislation API.

Parameters:
- `bill_number` (integer, required): Bill number (e.g., 1234 for HB1234, 5678 for SB5678)
- `biennium` (string, optional): Legislative biennium in format "YYYY-YY" (e.g., "2025-26"), defaults to current

Returns: Bill details including description, sponsor, status, fiscal notes, and companions.

### searchBills

Searches for bills using keywords and optional filtering via the WSL Search API.

Parameters:
- `query` (string, required): Search query text (e.g., "climate change", "transportation")
- `bienniums` (array, optional): List of bienniums to search (format: "YYYY-YY"), defaults to current
- `agency` (string, optional): Filter by originating agency ("House", "Senate", or "Both")
- `max_results` (integer, optional): Maximum number of total results to return (max 100)

Returns: List of bills matching the search criteria.

### getBillsByYear

Retrieves all bills from a specific year with optional filtering.

Parameters:
- `year` (string, optional): Year in format "YYYY" (e.g., "2025"), defaults to current
- `agency` (string, optional): Filter by originating agency ("House" or "Senate")
- `active_only` (boolean, optional): If true, only return active bills

Returns: List of bills matching the criteria.

### getBillStatus

Gets current status and history of a bill.

Parameters:
- `bill_number` (integer, required): Bill number (e.g., 1234 for HB1234)
- `biennium` (string, optional): Legislative biennium in format "YYYY-YY", defaults to current

Returns: Current status, history, action dates, and status descriptions.

### getBillDocuments

Retrieves bill document metadata with links to HTML and PDF versions.

Parameters:
- `bill_number` (integer, required): Bill number
- `biennium` (string, optional): Legislative biennium in format "YYYY-YY", defaults to current
- `document_type` (string, optional): Filter by type — "bill", "amendment", or "report"

Returns: Document metadata with links to HTML and PDF versions.

### getBillContent

Retrieves the actual content of a bill in an AI-friendly format.

Parameters:
- `bill_number` (integer, required): Bill number as an integer (e.g., 1234 for HB1234)
- `biennium` (string, optional): Legislative biennium in format "YYYY-YY", defaults to current
- `chamber` (string, optional): "House" or "Senate" (optional if bill number is unique across chambers)
- `bill_format` (string, optional): Document format — "xml" (default), "htm", or "pdf"

Returns: For XML and HTM: document content and metadata. For PDF: URL to access the document.

### getBillAmendments

Get amendments for a specific bill.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234")
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of amendments with sponsor, description, and status.

### getCommittees

Get committee information.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of committees.

## Roll Call and Voting Tools (1 tool)

### getRollCalls

Get roll call voting records for a bill with individual legislator votes.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB 1234" or "SB 5678")
- `biennium` (string, optional): Legislative biennium in format "YYYY-YY", defaults to current

Returns: Roll call votes with legislator names, vote values (yea/nay/absent/excused), dates, and descriptions.

## Amendment Tools (2 tools)

### getAmendmentsForBiennium

Get amendments for a bill in a biennium.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234")
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of amendments with sponsor, description, and status.

### getAmendmentsForYear

Get amendments for a bill in a specific year.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234")
- `year` (string, required): Year in format "YYYY" or "YY"

Returns: List of amendments for the specified year.

## Committee Tools (9 tools)

### getCommitteeMeetings

Get committee meeting schedules and agendas.

Parameters:
- `start_date` (string, required): Start date in YYYY-MM-DD format
- `end_date` (string, required): End date in YYYY-MM-DD format
- `committee` (string, optional): Filter by specific committee

Returns: List of committee meetings with dates, times, locations, and agenda items.

### getActiveCommittees

Get all currently active committees for both chambers.

Parameters: None

Returns: List of active committees.

### getActiveHouseCommittees

Get active House committees.

Parameters: None

Returns: List of active House committees.

### getActiveSenateCommittees

Get active Senate committees.

Parameters: None

Returns: List of active Senate committees.

### getActiveCommitteeMembers

Get members of an active committee.

Parameters:
- `committee_name` (string, required): Committee name

Returns: List of members with names, roles, party, district, and contact information.

### getCommitteeMembers

Get committee members for a biennium (historical).

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"
- `committee_name` (string, required): Committee name

Returns: List of committee members for the specified biennium.

### getHouseCommittees

Get all House committees for a biennium.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of House committees.

### getSenateCommittees

Get all Senate committees for a biennium.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of Senate committees.

### getCommitteeMeetingItems

Get agenda items for a specific committee meeting.

Parameters:
- `meeting_id` (string, required): Meeting identifier

Returns: List of agenda items for the meeting.

## Committee Action Tools (6 tools)

### getCommitteeExecutiveActionsByBill

Get executive actions taken on a bill by committees.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234")
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of executive actions with committee, date, and action type.

### getCommitteeReferralsByBill

Get committee referrals for a bill.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234")
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of referrals with committees and dates.

### getCommitteeReferralsByCommittee

Get bills referred to a specific committee.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"
- `committee_name` (string, required): Committee name (e.g., "House Finance")

Returns: List of bills referred to the committee.

### getDoPassByCommittee

Get bills with "do pass" recommendation from a committee.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"
- `committee_name` (string, required): Committee name

Returns: List of bills that received a do pass recommendation.

### getInCommittee

Get bills currently in a committee.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"
- `committee_name` (string, required): Committee name

Returns: List of bills currently referred to the committee.

### getLegislationReportedOutOfCommittee

Get bills reported out of a committee with recommendations.

Parameters:
- `committee_name` (string, required): Committee name
- `begin_date` (string, required): Begin date in YYYY-MM-DD format
- `end_date` (string, required): End date in YYYY-MM-DD format

Returns: List of bills reported out with recommendation type and vote counts.

## Session Law and RCW Tools (7 tools)

### getSessionLawByBill

Get session law information for a bill.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234")
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: Session law with chapter number, effective date, and law text reference.

### getSessionLawByBillId

Get session law by bill ID.

Parameters:
- `bill_id` (string, required): Bill ID (e.g., "HB 1234")
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: Session law information.

### getBillByChapterNumber

Get bill information by session law chapter number.

Parameters:
- `year` (integer, required): Year (e.g., 2025)
- `session` (integer, required): Session code (0=Regular, 1=1st Special, etc.)
- `chapter_number` (integer, required): Chapter number

Returns: Bill information for the specified chapter.

### getChapterNumbersByYear

Get all session law chapters for a year.

Parameters:
- `year` (integer, required): Year (e.g., 2025)

Returns: List of all session law chapters enacted that year.

### getSessionLawByInitiativeNumber

Get session law for an initiative.

Parameters:
- `initiative_number` (integer, required): Initiative number (e.g., 1234 for I-1234)

Returns: Initiative session law information.

### getRcwCitesAffected

Get RCW sections affected by a bill.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234")
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of RCW citations with section numbers and action types (amended, repealed, created).

### getHearings

Get committee hearings for a bill.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234")
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of hearings with committee, date, time, location, and agenda items.

## Governor Action Tools (3 tools)

### getLegislationGovernorSigned

Get bills signed by the governor.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of signed bills with action dates.

### getLegislationGovernorVeto

Get bills vetoed by the governor.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of vetoed bills with veto messages.

### getLegislationGovernorPartialVeto

Get bills with line-item vetoes by the governor.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of partially vetoed bills with affected sections.

## Sponsor and Legislator Tools (5 tools)

### findLegislator

Find legislators by district, chamber, or biennium.

Parameters:
- `biennium` (string, optional): Legislative biennium in format "YYYY-YY", defaults to current
- `chamber` (string, optional): "house" or "senate"
- `district` (string, optional): Legislative district number

Returns: List of legislators with name, party, district, and contact information.

### getSponsors

Get all sponsors for a biennium.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of sponsors for both chambers with contact information.

### getHouseSponsors

Get House sponsors.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of House sponsors.

### getSenateSponsors

Get Senate sponsors.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of Senate sponsors.

### getRequesters

Get entities authorized to request legislation.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of requesters.

## Bill Passage and Status Tools (5 tools)

### getLegislationPassedHouse

Get bills that passed the House.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of House-passed bills with passage dates and vote counts.

### getLegislationPassedSenate

Get bills that passed the Senate.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of Senate-passed bills with passage dates and vote counts.

### getLegislationPassedLegislature

Get bills that passed both chambers.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of bills that passed both House and Senate.

### getPrefiledLegislation

Get prefiled bills.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of prefiled bills with filing dates and sponsors.

### getLegislativeStatusChanges

Get bill status changes in a date range.

Parameters:
- `begin_date` (string, required): Begin date in YYYY-MM-DD format
- `end_date` (string, required): End date in YYYY-MM-DD format
- `biennium` (string, optional): Filter by biennium

Returns: List of status changes with old/new status and dates.

## Document Management Tools (3 tools)

### getDocumentClasses

Get available document types for a biennium.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"

Returns: List of document classes with names and descriptions.

### getAllDocumentsByClass

Get all documents of a specific class.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"
- `document_class` (string, required): Document class (e.g., "Bills", "Amendments")

Returns: List of documents with names, URLs, and bill associations.

### getDocumentsByClass

Get documents by class with name filter.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"
- `document_class` (string, required): Document class
- `name_filter` (string, required): Pattern to match (e.g., "HB 1*")

Returns: List of filtered documents.

## Metadata and Reference Tools (4 tools)

### getLegislationTypes

Get valid legislation types. Results are cached for 24 hours.

Parameters: None

Returns: List of legislation type codes and descriptions.

### getLegislationByRequestNumber

Look up bill by request number.

Parameters:
- `biennium` (string, required): Legislative biennium in format "YYYY-YY"
- `request_number` (string, required): Request number (e.g., "23-1234")

Returns: Bill information or request status.

### getRevisedCommitteeMeetings

Get committee meetings revised since a date.

Parameters:
- `since_date` (string, required): Date in YYYY-MM-DD format
- `biennium` (string, optional): Filter by biennium

Returns: List of revised meetings.

### getCommitteeMeetingItems

Get agenda items for a specific committee meeting.

Parameters:
- `meeting_id` (string, required): Meeting identifier

Returns: List of agenda items.

## MCP Resources

The server provides direct access to bill documents through URI templates:

### bill://xml/{biennium}/{chamber}/{bill_number}

Access bill documents in structured XML format (recommended for AI processing).

- `biennium`: Legislative biennium in format "YYYY-YY" (e.g., "2025-26")
- `chamber`: "House" or "Senate"
- `bill_number`: Bill number as numeric string (e.g., "1234")

### bill://htm/{biennium}/{chamber}/{bill_number}

Access bill documents in HTML format with hyperlinks to referenced laws.

### bill://pdf/{biennium}/{chamber}/{bill_number}

Get URLs for bill PDF documents (content not fetched directly).

### bill://document/{format}/{biennium}/{chamber}/{bill_number}

Generic format for accessing bill documents. `format` can be "xml", "htm", or "pdf".
