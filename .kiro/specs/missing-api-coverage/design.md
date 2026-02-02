# Design Document: Missing API Coverage

## Overview

This design expands the Washington State Legislature MCP Server to provide comprehensive coverage of the WSLWS SOAP APIs. The expansion adds 25+ new MCP tools organized into logical service groups: roll call votes, amendments, committee actions, session laws, governor actions, enhanced sponsor/committee information, and document management.

The design follows the existing architecture pattern: FastMCP tools that delegate to WSLClient for SOAP API calls, with consistent error handling, logging, and return types. New tools integrate seamlessly with existing functionality while adding powerful capabilities for civic engagement and legislative research.

### Design Principles

1. **Consistency**: Follow existing patterns for tool naming, parameters, and return types
2. **Usability**: Provide sensible defaults and clear parameter descriptions
3. **Robustness**: Comprehensive error handling with descriptive messages
4. **Performance**: Caching for reference data, pagination for large results
5. **Maintainability**: Clear separation between MCP tools and SOAP client logic

## Architecture

### System Components

The expansion maintains the existing three-layer architecture:

```
┌─────────────────────────────────────────┐
│         AI Assistant (MCP Client)       │
└─────────────────┬───────────────────────┘
                  │ MCP Protocol
┌─────────────────▼───────────────────────┐
│         FastMCP Server Layer            │
│  - Tool registration and routing        │
│  - Parameter validation                 │
│  - Response formatting                  │
└─────────────────┬───────────────────────┘
                  │ Python function calls
┌─────────────────▼───────────────────────┐
│         WSLClient (SOAP Layer)          │
│  - SOAP request construction            │
│  - API authentication                   │
│  - Response parsing                     │
│  - Connection pooling                   │
└─────────────────┬───────────────────────┘
                  │ SOAP/HTTP
┌─────────────────▼───────────────────────┐
│    WSLWS APIs (wslwebservices.leg.wa)   │
│  - LegislationService                   │
│  - SponsorService                       │
│  - CommitteeService                     │
│  - CommitteeActionService               │
│  - SessionLawService                    │
│  - AmendmentService                     │
│  - CommitteeMeetingService              │
│  - LegislativeDocumentService           │
└─────────────────────────────────────────┘
```

### Integration Points


**Existing Components to Reuse:**
- WSLClient: SOAP client with connection pooling and error handling
- FastMCP server instance: Tool registration and routing
- Logging configuration: Structured logging with context
- Error handling patterns: Try-catch with descriptive messages

**New Components to Add:**
- 25+ new MCP tool functions
- WSLClient methods for new SOAP operations
- Caching layer for reference data (legislation types, document classes)
- Pagination utilities for large result sets

## Components and Interfaces

### MCP Tool Organization

Tools are organized into logical groups matching WSLWS service boundaries:

#### 1. Roll Call and Voting Tools

**getRollCalls**
- Purpose: Get roll call votes for a bill
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
  - `bill_number` (str, required): e.g., "HB 1234"
- Returns: Dict with roll call list including legislator names, votes, dates
- WSLWS API: LegislationService.GetRollCalls

#### 2. Amendment Tools

**getAmendmentsForBiennium**
- Purpose: Get amendments for a bill in a biennium
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
  - `bill_number` (str, required): e.g., "SB 5678"
- Returns: Dict with amendment list including number, sponsor, description, status
- WSLWS API: LegislationService.GetAmendmentsForBiennium

**getAmendmentsForYear**
- Purpose: Get amendments for a bill in a specific year
- Parameters:
  - `year` (str, required): e.g., "2023" or "23"
  - `bill_number` (str, required): e.g., "HB 1234"
- Returns: Dict with amendment list
- WSLWS API: LegislationService.GetAmendmentsForYear


#### 3. Committee Hearing Tools

**getHearings**
- Purpose: Get committee hearings for a bill
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
  - `bill_number` (str, required): e.g., "HB 1234"
- Returns: Dict with hearing list including committee, date, time, location, agenda
- WSLWS API: LegislationService.GetHearings

#### 4. RCW Citation Tools

**getRcwCitesAffected**
- Purpose: Get RCW sections affected by a bill
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
  - `bill_number` (str, required): e.g., "SB 5678"
- Returns: Dict with RCW citations including section numbers and action types
- WSLWS API: LegislationService.GetRcwCitesAffected

#### 5. Session Law Tools

**getSessionLawByBill**
- Purpose: Get session law information for a bill
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
  - `bill_number` (str, required): e.g., "HB 1234"
- Returns: Dict with chapter number, effective date, law text reference
- WSLWS API: SessionLawService.GetSessionLawByBill

**getSessionLawByBillId**
- Purpose: Get session law by bill ID
- Parameters:
  - `bill_id` (int, required): Internal bill ID
- Returns: Dict with session law information
- WSLWS API: SessionLawService.GetSessionLawByBillId

**getBillByChapterNumber**
- Purpose: Get bill information by session law chapter number
- Parameters:
  - `year` (str, required): e.g., "2023"
  - `chapter_number` (str, required): e.g., "123"
- Returns: Dict with bill information
- WSLWS API: SessionLawService.GetBillByChapterNumber

**getChapterNumbersByYear**
- Purpose: Get all session law chapters for a year
- Parameters:
  - `year` (str, required): e.g., "2023"
- Returns: Dict with list of chapters
- WSLWS API: SessionLawService.GetChapterNumbersByYear

**getSessionLawByInitiativeNumber**
- Purpose: Get session law for an initiative
- Parameters:
  - `initiative_number` (str, required): e.g., "I-1234"
  - `year` (str, required): e.g., "2023"
- Returns: Dict with initiative session law information
- WSLWS API: SessionLawService.GetSessionLawByInitiativeNumber


#### 6. Governor Action Tools

**getLegislationGovernorSigned**
- Purpose: Get bills signed by the governor
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
- Returns: Dict with list of signed bills including dates
- WSLWS API: LegislationService.GetLegislationGovernorSigned

**getLegislationGovernorVeto**
- Purpose: Get bills vetoed by the governor
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
- Returns: Dict with list of vetoed bills including veto messages
- WSLWS API: LegislationService.GetLegislationGovernorVeto

**getLegislationGovernorPartialVeto**
- Purpose: Get bills partially vetoed by the governor
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
- Returns: Dict with list of partially vetoed bills and affected sections
- WSLWS API: LegislationService.GetLegislationGovernorPartialVeto

#### 7. Committee Action Tools

**getCommitteeExecutiveActionsByBill**
- Purpose: Get executive actions taken on a bill by committees
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
  - `bill_number` (str, required): e.g., "HB 1234"
- Returns: Dict with executive actions including committee, date, action type
- WSLWS API: CommitteeActionService.GetCommitteeExecutiveActionsByBill

**getCommitteeReferralsByBill**
- Purpose: Get committee referrals for a bill
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
  - `bill_number` (str, required): e.g., "SB 5678"
- Returns: Dict with referral history including committees and dates
- WSLWS API: CommitteeActionService.GetCommitteeReferralsByBill

**getCommitteeReferralsByCommittee**
- Purpose: Get bills referred to a specific committee
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
  - `committee_name` (str, required): e.g., "House Finance"
- Returns: Dict with list of referred bills
- WSLWS API: CommitteeActionService.GetCommitteeReferralsByCommittee

**getDoPassByCommittee**
- Purpose: Get bills with "do pass" recommendation from a committee
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
  - `committee_name` (str, required): e.g., "Senate Ways & Means"
- Returns: Dict with bills that received do pass recommendation
- WSLWS API: CommitteeActionService.GetDoPassByCommittee

**getInCommittee**
- Purpose: Get bills currently in a committee
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
  - `committee_name` (str, required): e.g., "House Education"
- Returns: Dict with bills currently referred to committee
- WSLWS API: CommitteeActionService.GetInCommittee

**getLegislationReportedOutOfCommittee**
- Purpose: Get bills reported out of a committee
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
  - `committee_name` (str, required): e.g., "Senate Law & Justice"
- Returns: Dict with bills reported out including recommendation and votes
- WSLWS API: CommitteeActionService.GetLegislationReportedOutOfCommittee


#### 8. Enhanced Committee Information Tools

**getActiveCommittees**
- Purpose: Get all currently active committees
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
- Returns: Dict with active committees for both chambers
- WSLWS API: CommitteeService.GetActiveCommittees

**getActiveHouseCommittees**
- Purpose: Get active House committees
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
- Returns: Dict with active House committees
- WSLWS API: CommitteeService.GetActiveHouseCommittees

**getActiveSenateCommittees**
- Purpose: Get active Senate committees
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
- Returns: Dict with active Senate committees
- WSLWS API: CommitteeService.GetActiveSenateCommittees

**getActiveCommitteeMembers**
- Purpose: Get members of an active committee
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
  - `committee_name` (str, required): e.g., "House Finance"
- Returns: Dict with member names, roles, party, district
- WSLWS API: CommitteeService.GetActiveCommitteeMembers

**getCommitteeMembers**
- Purpose: Get committee members for a biennium (historical)
- Parameters:
  - `biennium` (str, required): e.g., "2021-22"
  - `committee_name` (str, required): e.g., "Senate Transportation"
- Returns: Dict with committee membership information
- WSLWS API: CommitteeService.GetCommitteeMembers

**getHouseCommittees**
- Purpose: Get all House committees for a biennium
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
- Returns: Dict with House committee list
- WSLWS API: CommitteeService.GetHouseCommittees

**getSenateCommittees**
- Purpose: Get all Senate committees for a biennium
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
- Returns: Dict with Senate committee list
- WSLWS API: CommitteeService.GetSenateCommittees


#### 9. Enhanced Sponsor Tools

**getSponsors**
- Purpose: Get all sponsors for a biennium
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
- Returns: Dict with sponsor information for both chambers
- WSLWS API: SponsorService.GetSponsors

**getHouseSponsors**
- Purpose: Get House sponsors
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
- Returns: Dict with House sponsor information
- WSLWS API: SponsorService.GetHouseSponsors

**getSenateSponors**
- Purpose: Get Senate sponsors
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
- Returns: Dict with Senate sponsor information
- WSLWS API: SponsorService.GetSenateSponsors

**getRequesters**
- Purpose: Get entities authorized to request legislation
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
- Returns: Dict with requester information
- WSLWS API: SponsorService.GetRequesters

#### 10. Bill Passage and Status Tools

**getLegislationPassedHouse**
- Purpose: Get bills that passed the House
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
- Returns: Dict with House-passed bills including passage dates and votes
- WSLWS API: LegislationService.GetLegislationPassedHouse

**getLegislationPassedSenate**
- Purpose: Get bills that passed the Senate
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
- Returns: Dict with Senate-passed bills including passage dates and votes
- WSLWS API: LegislationService.GetLegislationPassedSenate

**getLegislationPassedLegislature**
- Purpose: Get bills that passed both chambers
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
- Returns: Dict with bills that passed both House and Senate
- WSLWS API: LegislationService.GetLegislationPassedLegislature

**getPrefiledLegislation**
- Purpose: Get prefiled bills
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
- Returns: Dict with prefiled bills including filing dates
- WSLWS API: LegislationService.GetPrefiledLegislation

**getLegislativeStatusChanges**
- Purpose: Get bill status changes in a date range
- Parameters:
  - `begin_date` (str, required): ISO 8601 format, e.g., "2023-01-01"
  - `end_date` (str, required): ISO 8601 format, e.g., "2023-12-31"
  - `biennium` (str, optional): Filter by biennium
- Returns: Dict with status changes including old/new status and dates
- WSLWS API: LegislationService.GetLegislativeStatusChanges


#### 11. Document Management Tools

**getDocumentClasses**
- Purpose: Get available document types for a biennium
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
- Returns: Dict with document class list including names and descriptions
- WSLWS API: LegislativeDocumentService.GetDocumentClasses

**getAllDocumentsByClass**
- Purpose: Get all documents of a specific class
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
  - `document_class` (str, required): e.g., "Bills", "Amendments"
- Returns: Dict with document list including names, URLs, bill associations
- WSLWS API: LegislativeDocumentService.GetAllDocumentsByClass

**getDocumentsByClass**
- Purpose: Get documents by class with name filter
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
  - `document_class` (str, required): e.g., "Bills"
  - `name_filter` (str, required): Pattern to match, e.g., "HB 1*"
- Returns: Dict with filtered document list
- WSLWS API: LegislativeDocumentService.GetDocumentsByClass

#### 12. Metadata and Reference Tools

**getLegislationTypes**
- Purpose: Get valid legislation types
- Parameters: None (cached for 24 hours)
- Returns: Dict with legislation type codes and descriptions
- WSLWS API: LegislationService.GetLegislationTypes

**getLegislationByRequestNumber**
- Purpose: Look up bill by original request number
- Parameters:
  - `biennium` (str, required): e.g., "2023-24"
  - `request_number` (str, required): e.g., "23-1234"
- Returns: Dict with bill information or request status
- WSLWS API: LegislationService.GetLegislationByRequestNumber

**getCommitteeMeetingItems**
- Purpose: Get agenda items for a specific committee meeting
- Parameters:
  - `meeting_id` (int, required): Meeting identifier
- Returns: Dict with agenda items including bills and topics
- WSLWS API: CommitteeMeetingService.GetCommitteeMeetingItems

**getRevisedCommitteeMeetings**
- Purpose: Get committee meetings revised since a date
- Parameters:
  - `since_date` (str, required): ISO 8601 format, e.g., "2023-01-01"
  - `biennium` (str, optional): Filter by biennium
- Returns: Dict with revised meetings
- WSLWS API: CommitteeMeetingService.GetRevisedCommitteeMeetings


## Data Models

### Common Data Structures

All tools return `Dict[str, Any]` with consistent structure:

```python
{
    "success": bool,           # Operation success indicator
    "data": Any,               # Actual response data (list or dict)
    "error": Optional[str],    # Error message if success=False
    "metadata": {              # Optional metadata
        "cached": bool,        # Whether response was cached
        "api_call": str,       # WSLWS API operation called
        "timestamp": str       # ISO 8601 timestamp
    }
}
```

### Roll Call Vote Structure

```python
{
    "bill_number": str,
    "roll_calls": [
        {
            "sequence_number": int,
            "date": str,              # ISO 8601
            "description": str,       # e.g., "Final Passage"
            "yea_votes": int,
            "nay_votes": int,
            "absent_votes": int,
            "excused_votes": int,
            "votes": [
                {
                    "legislator_name": str,
                    "vote": str,      # "Yea", "Nay", "Absent", "Excused"
                    "district": str,
                    "party": str
                }
            ]
        }
    ]
}
```

### Amendment Structure

```python
{
    "bill_number": str,
    "amendments": [
        {
            "amendment_number": str,
            "floor_number": str,
            "sponsor": str,
            "description": str,
            "status": str,
            "action_date": str        # ISO 8601
        }
    ]
}
```

### Committee Hearing Structure

```python
{
    "bill_number": str,
    "hearings": [
        {
            "committee_name": str,
            "committee_acronym": str,
            "date": str,              # ISO 8601
            "time": str,
            "location": str,
            "revised": bool,
            "cancelled": bool,
            "agenda_items": [str]
        }
    ]
}
```

### RCW Citation Structure

```python
{
    "bill_number": str,
    "rcw_cites": [
        {
            "rcw_section": str,       # e.g., "28A.150.260"
            "action_type": str,       # "Amended", "Repealed", "Created", "Reenacted"
            "chapter": str,
            "section": str
        }
    ]
}
```


### Session Law Structure

```python
{
    "bill_number": str,
    "session_law": {
        "chapter_number": str,
        "year": str,
        "effective_date": str,    # ISO 8601
        "partial_veto": bool,
        "vetoed_sections": [str],
        "law_text_url": str
    }
}
```

### Committee Structure

```python
{
    "committees": [
        {
            "name": str,
            "acronym": str,
            "agency": str,            # "House" or "Senate"
            "phone": str,
            "active": bool,
            "members": [
                {
                    "name": str,
                    "role": str,      # "Chair", "Vice Chair", "Member"
                    "party": str,
                    "district": str,
                    "email": str,
                    "phone": str
                }
            ]
        }
    ]
}
```

### Sponsor Structure

```python
{
    "sponsors": [
        {
            "name": str,
            "party": str,
            "district": str,
            "agency": str,            # "House" or "Senate"
            "email": str,
            "phone": str,
            "bills_sponsored": int    # Optional aggregate count
        }
    ]
}
```

### Status Change Structure

```python
{
    "status_changes": [
        {
            "bill_number": str,
            "biennium": str,
            "change_date": str,       # ISO 8601
            "old_status": str,
            "new_status": str,
            "action_description": str
        }
    ]
}
```

### Document Structure

```python
{
    "documents": [
        {
            "name": str,
            "document_class": str,
            "url": str,
            "bill_number": Optional[str],
            "date": str,              # ISO 8601
            "description": str
        }
    ]
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After analyzing all acceptance criteria, I identified several areas of redundancy:

1. **Data Structure Validation**: Many criteria (1.2, 2.3, 3.2, 4.2, 6.4, 7.5, 8.2, 8.5, 9.4, 10.2, 11.4, 12.2, 13.4, 13.5, 14.2, 15.2) all test that responses contain required fields. These can be consolidated into a single comprehensive property about response structure validation.

2. **Empty Result Handling**: Multiple edge cases (1.4, 2.4, 3.4, 4.4, 5.5, 10.4, 12.5) test that empty results return descriptive messages. This is a single pattern that applies across all tools.

3. **Chronological Ordering**: Criteria 1.3 and 3.3 both test chronological ordering of results. These can be combined into one property about temporal ordering.

4. **Chamber Filtering**: Criteria 8.3, 9.2, 12.4 all test chamber-based filtering. This is a single filtering pattern.

5. **Year/Biennium Filtering**: Criteria 6.5, 10.3, 11.5, 12.3, 15.5 all test temporal filtering. This is a single filtering pattern.

6. **Error Handling**: Criteria 1.5, 15.4, 16.2, 16.4 all test error handling. These can be consolidated into comprehensive error handling properties.

After consolidation, the following properties provide unique validation value:


### Core Data Retrieval Properties

**Property 1: Response Structure Consistency**
*For any* MCP tool call that returns data successfully, the response SHALL have the structure `{"success": True, "data": Any, "metadata": dict}` with all required fields for that data type present (e.g., roll calls include legislator names and votes, amendments include sponsor and status, committees include name and agency).
**Validates: Requirements 1.2, 2.3, 3.2, 4.2, 6.4, 7.5, 8.2, 8.5, 9.4, 10.2, 11.4, 12.2, 13.4, 13.5, 14.2, 15.2**

**Property 2: Empty Result Handling**
*For any* MCP tool call that returns no data (empty list), the response SHALL have `{"success": True, "data": [], "metadata": {"message": str}}` where the message describes why no results were found.
**Validates: Requirements 1.4, 2.4, 3.4, 4.4, 5.5, 10.4, 12.5**

**Property 3: Error Handling Consistency**
*For any* MCP tool call that encounters an error (invalid parameters, API failure, SOAP fault), the response SHALL have `{"success": False, "error": str}` where the error message is descriptive and does not expose internal implementation details.
**Validates: Requirements 1.5, 15.4, 16.2, 16.4**

### Data Ordering and Filtering Properties

**Property 4: Chronological Ordering**
*For any* MCP tool response containing time-ordered data (roll calls, hearings, status changes), the items SHALL be ordered by date in ascending chronological order.
**Validates: Requirements 1.3, 3.3**

**Property 5: Chamber Filtering Correctness**
*For any* MCP tool that accepts a chamber filter parameter (House/Senate), all returned items SHALL belong only to the specified chamber, and no items from the other chamber SHALL be included.
**Validates: Requirements 8.3, 9.2, 12.4**

**Property 6: Temporal Filtering Correctness**
*For any* MCP tool that accepts temporal filters (year, biennium, date range), all returned items SHALL fall within the specified time period, and no items outside that period SHALL be included.
**Validates: Requirements 6.5, 10.3, 11.5, 12.3, 15.5**

**Property 7: RCW Citation Grouping**
*For any* bill with multiple RCW citations, the citations SHALL be organized by action type (Amended, Repealed, Created, Reenacted), with all citations of the same type grouped together.
**Validates: Requirements 4.3**

### Format and Validation Properties

**Property 8: Year Format Flexibility**
*For any* MCP tool that accepts a year parameter, both 2-digit format (e.g., "23") and 4-digit format (e.g., "2023") SHALL be accepted and SHALL produce equivalent results.
**Validates: Requirements 2.5**

**Property 9: ISO 8601 Date Acceptance**
*For any* MCP tool that accepts date parameters, dates in ISO 8601 format (e.g., "2023-01-15") SHALL be accepted and parsed correctly.
**Validates: Requirements 10.5**

**Property 10: RCW Notation Formatting**
*For any* RCW citation returned by the system, the section SHALL be formatted in standard RCW notation (e.g., "28A.150.260" with chapter, title, and section components).
**Validates: Requirements 4.5**

### Specific Retrieval Properties

**Property 11: Roll Call Vote Completeness**
*For any* bill with roll call votes, calling getRollCalls SHALL return all recorded votes for that bill, with each vote including legislator name, vote value, and date.
**Validates: Requirements 1.1**

**Property 12: Amendment Retrieval by Biennium**
*For any* bill and biennium, calling getAmendmentsForBiennium SHALL return all amendments proposed for that bill during that biennium.
**Validates: Requirements 2.1**

**Property 13: Amendment Retrieval by Year**
*For any* bill and year, calling getAmendmentsForYear SHALL return all amendments proposed for that bill during that year.
**Validates: Requirements 2.2**

**Property 14: Hearing Retrieval Completeness**
*For any* bill, calling getHearings SHALL return all scheduled and past committee hearings for that bill, including revised meetings indicated with a revised flag.
**Validates: Requirements 3.1, 3.5**

**Property 15: RCW Citation Retrieval**
*For any* bill, calling getRcwCitesAffected SHALL return all RCW sections affected by that bill with their action types.
**Validates: Requirements 4.1**

**Property 16: Session Law Retrieval by Bill**
*For any* enacted bill, calling getSessionLawByBill SHALL return the chapter number, effective date, and law text reference.
**Validates: Requirements 5.1**

**Property 17: Session Law Reverse Lookup**
*For any* valid chapter number and year, calling getBillByChapterNumber SHALL return the corresponding bill information.
**Validates: Requirements 5.2**

**Property 18: Annual Session Law Completeness**
*For any* year, calling getChapterNumbersByYear SHALL return all session laws enacted during that year.
**Validates: Requirements 5.3**

**Property 19: Initiative Session Law Retrieval**
*For any* initiative number and year, calling getSessionLawByInitiativeNumber SHALL return initiative-specific session law data.
**Validates: Requirements 5.4**


### Governor Action Properties

**Property 20: Governor Signed Bills Retrieval**
*For any* biennium, calling getLegislationGovernorSigned SHALL return all bills signed by the governor during that biennium with action dates.
**Validates: Requirements 6.1**

**Property 21: Governor Vetoed Bills Retrieval**
*For any* biennium, calling getLegislationGovernorVeto SHALL return all bills vetoed by the governor with veto messages included.
**Validates: Requirements 6.2**

**Property 22: Governor Partial Veto Retrieval**
*For any* biennium, calling getLegislationGovernorPartialVeto SHALL return all bills with line-item vetoes and the affected sections.
**Validates: Requirements 6.3**

### Committee Action Properties

**Property 23: Committee Action Retrieval**
*For any* bill, calling getCommitteeExecutiveActionsByBill and getCommitteeReferralsByBill SHALL return all executive actions and referrals for that bill.
**Validates: Requirements 7.1**

**Property 24: Bills in Committee Retrieval**
*For any* committee and biennium, calling getInCommittee SHALL return all bills currently referred to that committee.
**Validates: Requirements 7.2**

**Property 25: Do Pass Filtering**
*For any* committee and biennium, calling getDoPassByCommittee SHALL return only bills that received a "do pass" recommendation from that committee.
**Validates: Requirements 7.3**

**Property 26: Reported Bills Include Recommendations**
*For any* committee and biennium, calling getLegislationReportedOutOfCommittee SHALL return bills with recommendation type and vote counts included.
**Validates: Requirements 7.4**

### Committee Information Properties

**Property 27: Active Committee Retrieval**
*For any* biennium, calling getActiveCommittees SHALL return all currently active committees for both House and Senate.
**Validates: Requirements 8.1**

**Property 28: Historical Committee Composition**
*For any* biennium and committee name, calling getCommitteeMembers SHALL return the historical committee composition for that biennium.
**Validates: Requirements 8.4**

### Sponsor Properties

**Property 29: Sponsor Retrieval Completeness**
*For any* biennium, calling getSponsors SHALL return sponsor information for both chambers including name, party, district, and contact information.
**Validates: Requirements 9.1**

**Property 30: Requester Information Retrieval**
*For any* biennium, calling getRequesters SHALL return all entities authorized to request legislation.
**Validates: Requirements 9.3**

**Property 31: Sponsorship Count Aggregation**
*For any* sponsor with multiple bills, the sponsorship count SHALL equal the number of bills sponsored by that legislator.
**Validates: Requirements 9.5**

### Status Tracking Properties

**Property 32: Status Change Date Range Filtering**
*For any* date range, calling getLegislativeStatusChanges SHALL return all bills with status updates within that period, and no bills with updates outside that period.
**Validates: Requirements 10.1**

### Passage Tracking Properties

**Property 33: House Passage Retrieval**
*For any* biennium, calling getLegislationPassedHouse SHALL return all bills that passed the House during that biennium.
**Validates: Requirements 11.1**

**Property 34: Senate Passage Retrieval**
*For any* biennium, calling getLegislationPassedSenate SHALL return all bills that passed the Senate during that biennium.
**Validates: Requirements 11.2**

**Property 35: Legislature Passage Retrieval**
*For any* biennium, calling getLegislationPassedLegislature SHALL return only bills that passed both chambers.
**Validates: Requirements 11.3**

### Prefiled Legislation Properties

**Property 36: Prefiled Legislation Retrieval**
*For any* biennium, calling getPrefiledLegislation SHALL return all bills filed before the session start date.
**Validates: Requirements 12.1**

### Document Management Properties

**Property 37: Document Class Retrieval**
*For any* biennium, calling getDocumentClasses SHALL return all available document types for that biennium with class names and descriptions.
**Validates: Requirements 13.1, 13.5**

**Property 38: Document Class Filtering**
*For any* biennium and document class, calling getAllDocumentsByClass SHALL return all documents of that class.
**Validates: Requirements 13.2**

**Property 39: Document Name Pattern Matching**
*For any* biennium, document class, and name filter pattern, calling getDocumentsByClass SHALL return only documents whose names match the filter pattern.
**Validates: Requirements 13.3**

### Metadata Properties

**Property 40: Legislation Type Retrieval**
*For any* call to getLegislationTypes, the response SHALL include all valid legislation type codes with descriptions and chamber applicability.
**Validates: Requirements 14.1**

**Property 41: Legislation Type Caching**
*For any* sequence of calls to getLegislationTypes within 24 hours, only the first call SHALL make an API request, and subsequent calls SHALL return cached data with cache metadata.
**Validates: Requirements 14.3, 18.1, 18.5**

**Property 42: Legislation Type Validation**
*For any* tool that accepts a legislation type parameter, invalid types SHALL be rejected with a descriptive error before making API calls.
**Validates: Requirements 14.4**

**Property 43: Request Number Lookup**
*For any* valid request number and biennium, calling getLegislationByRequestNumber SHALL return the corresponding bill information or pending request status.
**Validates: Requirements 15.1, 15.2**

### Performance Properties

**Property 44: Pagination for Large Results**
*For any* tool response with more than 100 items, the results SHALL be paginated with configurable page size, and pagination metadata SHALL be included in the response.
**Validates: Requirements 18.3**

**Property 45: Timeout Handling**
*For any* API call that exceeds the configured timeout value, the tool SHALL return a timeout error with a descriptive message.
**Validates: Requirements 18.4**

### Integration Properties

**Property 46: Return Type Consistency**
*For any* MCP tool in the system (existing or new), the return type SHALL be `Dict[str, Any]` with consistent structure matching the common data structure pattern.
**Validates: Requirements 17.3**

**Property 47: Optional Parameter Defaults**
*For any* MCP tool with optional parameters, calling the tool without those parameters SHALL use sensible defaults and execute successfully.
**Validates: Requirements 17.4**


## Error Handling

### Error Categories

The system handles four categories of errors:

#### 1. Input Validation Errors
- **Trigger**: Invalid parameters before API call
- **Examples**: Missing required parameters, invalid date formats, invalid bill numbers
- **Handling**: Validate parameters, return `{"success": False, "error": "descriptive message"}` immediately
- **Logging**: Log validation failure with parameter values (sanitized)

#### 2. SOAP Fault Errors
- **Trigger**: WSLWS API returns SOAP fault
- **Examples**: Invalid bill number, biennium not found, service unavailable
- **Handling**: Extract fault message, return user-friendly error
- **Logging**: Log full SOAP fault with request context

#### 3. Network Errors
- **Trigger**: Connection failures, timeouts, DNS errors
- **Examples**: Network unreachable, connection timeout, DNS resolution failure
- **Handling**: Retry up to 3 times with exponential backoff (1s, 2s, 4s), then return error
- **Logging**: Log each retry attempt and final failure

#### 4. Unexpected Errors
- **Trigger**: Parsing errors, unexpected response format, Python exceptions
- **Examples**: XML parsing failure, missing expected fields, type errors
- **Handling**: Catch exception, return generic error, log full traceback
- **Logging**: Log full exception with stack trace and request context

### Error Response Format

All errors follow consistent format:

```python
{
    "success": False,
    "error": str,              # User-friendly error message
    "error_type": str,         # "validation", "api_fault", "network", "unexpected"
    "metadata": {
        "timestamp": str,      # ISO 8601
        "tool_name": str,      # MCP tool that failed
        "request_id": str      # Unique request identifier for log correlation
    }
}
```

### Retry Logic

Network errors trigger automatic retry with exponential backoff:

```python
def call_with_retry(api_func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return api_func()
        except NetworkError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            time.sleep(wait_time)
            logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s")
```

### Timeout Configuration

All API calls have configurable timeouts:

- **Default timeout**: 30 seconds
- **Long-running operations**: 60 seconds (bulk queries, document retrieval)
- **Quick operations**: 10 seconds (cached data, metadata)
- **Configuration**: Environment variable `WSLWS_TIMEOUT` or per-tool override

### Logging Strategy

Structured logging with context:

```python
logger.info("API call started", extra={
    "tool": "getRollCalls",
    "biennium": "2023-24",
    "bill_number": "HB 1234",
    "request_id": "abc123"
})

logger.error("API call failed", extra={
    "tool": "getRollCalls",
    "error_type": "api_fault",
    "error_message": "Bill not found",
    "request_id": "abc123"
}, exc_info=True)
```


## Testing Strategy

### Dual Testing Approach

The system requires both unit tests and property-based tests for comprehensive coverage:

- **Unit tests**: Verify specific examples, edge cases, and error conditions
- **Property tests**: Verify universal properties across all inputs
- Both are complementary and necessary

### Property-Based Testing

**Framework**: Use `hypothesis` library for Python property-based testing

**Configuration**:
- Minimum 100 iterations per property test
- Each test tagged with feature name and property number
- Tag format: `# Feature: missing-api-coverage, Property N: [property text]`

**Example Property Test**:

```python
from hypothesis import given, strategies as st
import pytest

@given(
    biennium=st.sampled_from(["2021-22", "2023-24", "2025-26"]),
    bill_number=st.from_regex(r"(HB|SB) \d{4}", fullmatch=True)
)
@pytest.mark.property_test
def test_roll_call_response_structure(biennium, bill_number):
    """
    Feature: missing-api-coverage, Property 1: Response Structure Consistency
    
    For any MCP tool call that returns data successfully, the response SHALL
    have the required structure with all mandatory fields present.
    """
    response = getRollCalls(biennium=biennium, bill_number=bill_number)
    
    # Verify response structure
    assert "success" in response
    assert "data" in response
    assert "metadata" in response
    
    if response["success"] and response["data"]:
        # Verify roll call data structure
        for roll_call in response["data"]:
            assert "sequence_number" in roll_call
            assert "date" in roll_call
            assert "votes" in roll_call
            for vote in roll_call["votes"]:
                assert "legislator_name" in vote
                assert "vote" in vote
```

**Property Test Coverage**:
- Each of the 47 correctness properties MUST have a corresponding property test
- Properties marked as "edge-case" in prework should be covered by unit tests
- Properties about logging and implementation details (16.1, 16.3, 16.5, 17.1, 17.2, 17.5, 18.2) are covered by integration tests

### Unit Testing

**Framework**: Use `pytest` for unit testing

**Unit Test Focus**:
- Specific examples demonstrating correct behavior
- Edge cases (empty results, missing data, boundary conditions)
- Error conditions (invalid inputs, API failures)
- Integration points between components

**Example Unit Tests**:

```python
def test_empty_roll_calls_returns_descriptive_message():
    """Test that bills with no roll calls return empty list with message."""
    # Property 2: Empty Result Handling
    response = getRollCalls(biennium="2023-24", bill_number="HB 9999")
    
    assert response["success"] is True
    assert response["data"] == []
    assert "message" in response["metadata"]
    assert "no roll calls" in response["metadata"]["message"].lower()

def test_invalid_bill_number_returns_error():
    """Test that invalid bill numbers are rejected with descriptive error."""
    # Property 3: Error Handling Consistency
    response = getRollCalls(biennium="2023-24", bill_number="INVALID")
    
    assert response["success"] is False
    assert "error" in response
    assert "invalid bill number" in response["error"].lower()

def test_year_format_flexibility():
    """Test that both 2-digit and 4-digit years work."""
    # Property 8: Year Format Flexibility
    response_2digit = getAmendmentsForYear(year="23", bill_number="HB 1234")
    response_4digit = getAmendmentsForYear(year="2023", bill_number="HB 1234")
    
    # Both should succeed and return equivalent data
    assert response_2digit["success"] == response_4digit["success"]
    if response_2digit["success"]:
        assert len(response_2digit["data"]) == len(response_4digit["data"])
```

### Integration Testing

**Focus**: Test interactions between MCP tools, WSLClient, and WSLWS APIs

**Integration Test Examples**:
- WSLClient connection pooling and reuse
- Caching behavior across multiple tool calls
- Retry logic with simulated network failures
- Logging output verification
- End-to-end flows (e.g., search bill → get roll calls → get session law)

### Test Organization

```
tests/
├── unit/
│   ├── test_roll_call_tools.py
│   ├── test_amendment_tools.py
│   ├── test_committee_tools.py
│   ├── test_session_law_tools.py
│   ├── test_governor_action_tools.py
│   ├── test_sponsor_tools.py
│   ├── test_document_tools.py
│   └── test_error_handling.py
├── property/
│   ├── test_response_structure_properties.py
│   ├── test_filtering_properties.py
│   ├── test_retrieval_properties.py
│   ├── test_caching_properties.py
│   └── test_validation_properties.py
├── integration/
│   ├── test_wslclient_integration.py
│   ├── test_caching_integration.py
│   ├── test_retry_logic.py
│   └── test_end_to_end_flows.py
└── conftest.py  # Shared fixtures and configuration
```

### Test Data Strategy

**Approach**: Use real WSLWS API data for testing when possible

**Test Data Sources**:
1. **Live API calls**: For integration tests (requires network)
2. **Recorded responses**: VCR.py for repeatable unit tests
3. **Generated data**: Hypothesis strategies for property tests
4. **Known examples**: Specific bills/bienniums with known characteristics

**Example Test Data**:
```python
# Known test cases
KNOWN_BILLS = {
    "with_roll_calls": ("2023-24", "HB 1001"),
    "with_amendments": ("2023-24", "SB 5001"),
    "passed_both_chambers": ("2023-24", "HB 1050"),
    "governor_signed": ("2023-24", "SB 5200"),
    "no_activity": ("2023-24", "HB 9999"),  # Likely doesn't exist
}
```

### Continuous Testing

**CI/CD Integration**:
- Run unit tests on every commit
- Run property tests (100 iterations) on every PR
- Run integration tests nightly
- Generate coverage reports (target: 90%+ for new code)

**Performance Benchmarks**:
- Track API response times
- Monitor cache hit rates
- Measure test suite execution time

### Test Coverage Goals

- **Unit test coverage**: 85%+ of new code
- **Property test coverage**: All 47 correctness properties
- **Integration test coverage**: All major workflows
- **Edge case coverage**: All identified edge cases from prework

