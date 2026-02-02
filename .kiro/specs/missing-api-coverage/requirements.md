# Requirements Document

## Introduction

This specification defines the expansion of the Washington State Legislature MCP Server to provide comprehensive coverage of the Washington State Legislative Web Services (WSLWS) SOAP APIs. The current implementation covers basic bill information, search, and committee meetings, but lacks critical functionality for roll call votes, committee actions, amendments, session laws, and enhanced sponsor/legislator information. This expansion will enable AI assistants to answer complex questions about the legislative process and support civic engagement use cases.

## Glossary

- **MCP**: Model Context Protocol - a protocol for AI assistants to access external data sources
- **WSLWS**: Washington State Legislative Web Services - SOAP-based APIs for legislative data
- **FastMCP**: Python framework for building MCP servers
- **WSLClient**: Existing SOAP client wrapper for WSLWS APIs
- **Biennium**: Two-year legislative session period (e.g., "2023-24")
- **RCW**: Revised Code of Washington - state statutes
- **Roll_Call**: Record of how legislators voted on a bill
- **Session_Law**: Final enacted law with chapter number
- **Amendment**: Proposed change to a bill
- **Committee_Action**: Actions taken by committees (referrals, executive actions, etc.)
- **Bill_Number**: Legislation identifier (e.g., "HB 1234", "SB 5678")
- **Agency**: Legislative chamber (House or Senate)
- **MCP_Tool**: Function exposed to AI assistants via MCP protocol

## Requirements

### Requirement 1: Roll Call Vote Access

**User Story:** As a civic engagement user, I want to access roll call voting records, so that I can see how legislators voted on specific bills.

#### Acceptance Criteria

1. WHEN a user requests roll calls for a bill, THE MCP_Tool SHALL retrieve all roll call votes for that bill
2. WHEN roll call data is returned, THE MCP_Tool SHALL include legislator names, vote values (yea/nay/absent/excused), and vote dates
3. WHEN a bill has multiple roll calls, THE MCP_Tool SHALL return all votes in chronological order
4. IF a bill has no roll calls, THEN THE MCP_Tool SHALL return an empty list with a descriptive message
5. WHEN the WSLWS API returns an error, THE MCP_Tool SHALL handle it gracefully and return an error message

### Requirement 2: Amendment Information Access

**User Story:** As a legislative researcher, I want to access amendments for bills, so that I can track proposed changes to legislation.

#### Acceptance Criteria

1. WHEN a user requests amendments for a biennium, THE MCP_Tool SHALL retrieve all amendments for the specified bill and biennium
2. WHEN a user requests amendments for a year, THE MCP_Tool SHALL retrieve all amendments for the specified bill and year
3. WHEN amendment data is returned, THE MCP_Tool SHALL include amendment number, sponsor, description, and status
4. WHEN a bill has no amendments, THE MCP_Tool SHALL return an empty list with a descriptive message
5. WHERE a user specifies a year, THE MCP_Tool SHALL accept both 2-digit and 4-digit year formats

### Requirement 3: Committee Hearing Information

**User Story:** As a citizen advocate, I want to see committee hearings for bills, so that I can participate in the legislative process.

#### Acceptance Criteria

1. WHEN a user requests hearings for a bill, THE MCP_Tool SHALL retrieve all scheduled and past hearings
2. WHEN hearing data is returned, THE MCP_Tool SHALL include committee name, date, time, location, and agenda items
3. WHEN a bill has multiple hearings, THE MCP_Tool SHALL return all hearings in chronological order
4. IF a bill has no hearings scheduled, THEN THE MCP_Tool SHALL return an empty list with a descriptive message
5. WHEN hearing information includes revised meetings, THE MCP_Tool SHALL indicate which meetings were updated

### Requirement 4: RCW Citations Affected

**User Story:** As a legal researcher, I want to see which RCW sections are affected by a bill, so that I can understand the statutory impact.

#### Acceptance Criteria

1. WHEN a user requests RCW citations for a bill, THE MCP_Tool SHALL retrieve all affected RCW sections
2. WHEN RCW citation data is returned, THE MCP_Tool SHALL include section numbers and action types (amended, repealed, created)
3. WHEN a bill affects multiple RCW sections, THE MCP_Tool SHALL return all citations organized by action type
4. IF a bill affects no RCW sections, THEN THE MCP_Tool SHALL return an empty list with a descriptive message
5. WHEN RCW citations include chapter and section numbers, THE MCP_Tool SHALL format them in standard RCW notation

### Requirement 5: Session Law Information

**User Story:** As a legal professional, I want to access session law information, so that I can reference enacted legislation by chapter number.

#### Acceptance Criteria

1. WHEN a user requests session law by bill, THE MCP_Tool SHALL retrieve chapter number, effective date, and law text reference
2. WHEN a user requests session law by chapter number, THE MCP_Tool SHALL retrieve the corresponding bill information
3. WHEN a user requests all chapters for a year, THE MCP_Tool SHALL return all session laws enacted that year
4. WHEN a user requests session law for an initiative, THE MCP_Tool SHALL retrieve initiative-specific session law data
5. IF a bill has not been enacted into law, THEN THE MCP_Tool SHALL return a message indicating no session law exists

### Requirement 6: Governor Actions

**User Story:** As a political analyst, I want to track governor actions on bills, so that I can analyze executive branch influence on legislation.

#### Acceptance Criteria

1. WHEN a user requests bills signed by the governor, THE MCP_Tool SHALL retrieve all signed bills for a biennium
2. WHEN a user requests bills vetoed by the governor, THE MCP_Tool SHALL retrieve all vetoed bills with veto messages
3. WHEN a user requests partially vetoed bills, THE MCP_Tool SHALL retrieve bills with line-item vetoes and affected sections
4. WHEN governor action data is returned, THE MCP_Tool SHALL include action date, bill number, and action type
5. WHERE a user filters by year, THE MCP_Tool SHALL return only bills with governor actions in that year

### Requirement 7: Committee Action Tracking

**User Story:** As a legislative tracker, I want to see detailed committee actions, so that I can monitor bill progress through committees.

#### Acceptance Criteria

1. WHEN a user requests committee actions for a bill, THE MCP_Tool SHALL retrieve all executive actions and referrals
2. WHEN a user requests bills in a specific committee, THE MCP_Tool SHALL return all currently referred bills
3. WHEN a user requests bills with "do pass" recommendations, THE MCP_Tool SHALL filter by committee and return matching bills
4. WHEN a user requests bills reported out of committee, THE MCP_Tool SHALL include the recommendation type and vote counts
5. WHEN committee action data is returned, THE MCP_Tool SHALL include action date, committee name, and action description

### Requirement 8: Enhanced Committee Information

**User Story:** As a constituent, I want to see committee membership and structure, so that I can contact relevant committee members.

#### Acceptance Criteria

1. WHEN a user requests active committees, THE MCP_Tool SHALL retrieve all currently active committees for both chambers
2. WHEN a user requests committee members, THE MCP_Tool SHALL return member names, roles (chair/vice-chair/member), and party affiliation
3. WHERE a user filters by chamber, THE MCP_Tool SHALL return only House or Senate committees as specified
4. WHEN a user requests committee structure for a biennium, THE MCP_Tool SHALL return historical committee composition
5. WHEN committee data is returned, THE MCP_Tool SHALL include committee name, acronym, phone, and agency

### Requirement 9: Enhanced Sponsor Information

**User Story:** As a researcher, I want comprehensive sponsor information, so that I can analyze sponsorship patterns and legislator activity.

#### Acceptance Criteria

1. WHEN a user requests all sponsors for a biennium, THE MCP_Tool SHALL retrieve sponsor information for both chambers
2. WHERE a user filters by chamber, THE MCP_Tool SHALL return only House or Senate sponsors as specified
3. WHEN a user requests requesters, THE MCP_Tool SHALL return entities authorized to request legislation
4. WHEN sponsor data is returned, THE MCP_Tool SHALL include name, party, district, and contact information
5. WHEN sponsor information includes sponsorship counts, THE MCP_Tool SHALL aggregate bills by sponsor

### Requirement 10: Bill Status Change Tracking

**User Story:** As a legislative monitor, I want to track bill status changes over time, so that I can receive updates on legislative activity.

#### Acceptance Criteria

1. WHEN a user requests status changes for a date range, THE MCP_Tool SHALL retrieve all bills with status updates in that period
2. WHEN status change data is returned, THE MCP_Tool SHALL include bill number, old status, new status, and change date
3. WHEN a user specifies a biennium filter, THE MCP_Tool SHALL return only status changes for that biennium
4. IF no status changes occurred in the date range, THEN THE MCP_Tool SHALL return an empty list with a descriptive message
5. WHEN date parameters are provided, THE MCP_Tool SHALL accept ISO 8601 date format

### Requirement 11: Bill Passage Tracking

**User Story:** As a policy analyst, I want to track bills that passed each chamber, so that I can analyze legislative productivity.

#### Acceptance Criteria

1. WHEN a user requests bills passed by the House, THE MCP_Tool SHALL retrieve all House-passed bills for a biennium
2. WHEN a user requests bills passed by the Senate, THE MCP_Tool SHALL retrieve all Senate-passed bills for a biennium
3. WHEN a user requests bills passed by the legislature, THE MCP_Tool SHALL retrieve bills that passed both chambers
4. WHEN passage data is returned, THE MCP_Tool SHALL include passage date, vote counts, and current status
5. WHERE a user filters by year, THE MCP_Tool SHALL return only bills passed in that year

### Requirement 12: Prefiled Legislation Access

**User Story:** As an early legislative tracker, I want to see prefiled bills, so that I can monitor upcoming legislative priorities.

#### Acceptance Criteria

1. WHEN a user requests prefiled legislation, THE MCP_Tool SHALL retrieve all bills filed before session start
2. WHEN prefiled bill data is returned, THE MCP_Tool SHALL include filing date, sponsor, and bill title
3. WHERE a user filters by biennium, THE MCP_Tool SHALL return only prefiled bills for that biennium
4. WHEN a user filters by chamber, THE MCP_Tool SHALL return only House or Senate prefiled bills
5. IF no prefiled bills exist for the criteria, THEN THE MCP_Tool SHALL return an empty list with a descriptive message

### Requirement 13: Document Class Management

**User Story:** As a document researcher, I want to browse documents by type, so that I can find specific legislative document categories.

#### Acceptance Criteria

1. WHEN a user requests document classes, THE MCP_Tool SHALL retrieve all available document types for a biennium
2. WHEN a user requests documents by class, THE MCP_Tool SHALL return all documents matching that class
3. WHERE a user provides a name filter, THE MCP_Tool SHALL return only documents matching the filter pattern
4. WHEN document data is returned, THE MCP_Tool SHALL include document name, URL, class, and bill association
5. WHEN document classes are listed, THE MCP_Tool SHALL include class name and description

### Requirement 14: Legislation Type Information

**User Story:** As a legislative system user, I want to see valid legislation types, so that I can understand bill categorization.

#### Acceptance Criteria

1. WHEN a user requests legislation types, THE MCP_Tool SHALL retrieve all valid types for the legislative system
2. WHEN legislation type data is returned, THE MCP_Tool SHALL include type code, description, and chamber applicability
3. THE MCP_Tool SHALL cache legislation types to minimize API calls
4. WHEN legislation types are used in other tools, THE MCP_Tool SHALL validate against the retrieved type list
5. IF the API returns no legislation types, THEN THE MCP_Tool SHALL return a default set with a warning

### Requirement 15: Request Number Lookup

**User Story:** As a legislative staff member, I want to look up bills by request number, so that I can track bills from initial request through introduction.

#### Acceptance Criteria

1. WHEN a user provides a request number, THE MCP_Tool SHALL retrieve the corresponding bill information
2. WHEN request number lookup succeeds, THE MCP_Tool SHALL return bill number, title, sponsor, and current status
3. IF a request number has not been assigned a bill number, THEN THE MCP_Tool SHALL return request information with pending status
4. WHEN a request number is invalid, THE MCP_Tool SHALL return a descriptive error message
5. WHERE a user provides a biennium, THE MCP_Tool SHALL search only within that biennium

### Requirement 16: Error Handling and Logging

**User Story:** As a system administrator, I want comprehensive error handling and logging, so that I can troubleshoot issues and monitor system health.

#### Acceptance Criteria

1. WHEN any WSLWS API call fails, THE MCP_Tool SHALL log the error with request parameters and error details
2. WHEN a SOAP fault occurs, THE MCP_Tool SHALL extract the fault message and return it to the user
3. WHEN network errors occur, THE MCP_Tool SHALL retry the request up to 3 times with exponential backoff
4. WHEN invalid parameters are provided, THE MCP_Tool SHALL validate and return descriptive error messages before making API calls
5. WHEN successful API calls complete, THE MCP_Tool SHALL log request parameters and response summary for monitoring

### Requirement 17: Integration with Existing Tools

**User Story:** As a developer, I want new tools to integrate seamlessly with existing functionality, so that the MCP server maintains consistency.

#### Acceptance Criteria

1. WHEN new tools are added, THE MCP_Tool SHALL follow existing naming conventions and parameter patterns
2. WHEN new tools use WSLClient, THE MCP_Tool SHALL reuse existing SOAP client instances and connection pooling
3. WHEN new tools return data, THE MCP_Tool SHALL use consistent Dict[str, Any] return types matching existing tools
4. WHEN new tools handle optional parameters, THE MCP_Tool SHALL provide sensible defaults consistent with existing tools
5. WHEN new tools are documented, THE MCP_Tool SHALL include parameter descriptions and examples matching existing tool documentation

### Requirement 18: Performance and Caching

**User Story:** As a system user, I want responsive tool performance, so that AI assistants can quickly answer questions.

#### Acceptance Criteria

1. WHEN reference data is requested (legislation types, document classes), THE MCP_Tool SHALL cache results for 24 hours
2. WHEN multiple related API calls are needed, THE MCP_Tool SHALL batch requests where possible
3. WHEN large result sets are returned, THE MCP_Tool SHALL implement pagination with configurable page size
4. WHEN API responses are slow, THE MCP_Tool SHALL implement timeout handling with configurable timeout values
5. WHEN cached data is used, THE MCP_Tool SHALL include cache metadata in the response
